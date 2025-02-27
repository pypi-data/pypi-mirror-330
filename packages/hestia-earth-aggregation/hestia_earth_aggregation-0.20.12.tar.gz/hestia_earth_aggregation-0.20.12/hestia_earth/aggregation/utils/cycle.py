from datetime import datetime
from functools import reduce
from hestia_earth.schema import (
    CycleStartDateDefinition, TermTermType, SchemaType, CycleDefaultMethodClassification
)
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.model import filter_list_term_type, find_term_match, find_primary_product
from hestia_earth.utils.tools import list_sum, non_empty_list, flatten, is_number, is_boolean

from hestia_earth.aggregation.log import logger
from . import (
    _aggregated_node, _aggregated_version, _set_dict_array, pick,
    format_aggregated_list
)
from .site import update_site
from .blank_node import cleanup_blank_nodes
from .completeness import aggregate_completeness, completeness_from_count
from .term import _format_country_name, _format_organic, _format_irrigated
from .group import group_by_term_id
from .source import format_aggregated_sources
from .emission import new_emission
from .input import new_input
from .practice import new_practice, organic_practice
from .product import new_product


def _timestamp(): return datetime.now().strftime('%Y%m%d')


def _is_organic(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'


def is_organic(cycle: dict):
    term_type = TermTermType.STANDARDSLABELS
    lookup = download_lookup(f"{term_type.value}.csv")
    practices = filter_list_term_type(cycle.get('practices', []), term_type)
    return any([_is_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def _is_irrigated(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name('irrigated'))


def is_irrigated(cycle: dict):
    term_type = TermTermType.WATERREGIME
    lookup = download_lookup(f"{term_type.value}.csv")
    practices = filter_list_term_type(cycle.get('practices', []), term_type)
    return any([
        list_sum(p.get('value', []), 0) > 0 for p in practices if _is_irrigated(lookup, p.get('term', {}).get('@id'))
    ])


def aggregate_with_matrix(product: dict):
    # only aggregate by organic / irrigated for `crop` products
    return product.get('termType') in [
        TermTermType.CROP.value
    ]


def _filter_practice(aggregate: dict):
    return all([
        aggregate.get('term').get('@id') not in ['organic'],
        is_number(aggregate.get('value')) or is_boolean(aggregate.get('value'))
    ])


def _format_aggregate(new_func, filter_func=None):
    def format(aggregate: dict):
        blank_node = new_func(aggregate)

        observations = aggregate.get('observations')
        _set_dict_array(blank_node, 'observations', observations)

        return _aggregated_version(blank_node) if all([
            blank_node is not None,
            filter_func is None or filter_func(aggregate)
        ]) else None
    return format


def _format_results(
    cycle: dict,
    site: dict,
    completeness: dict,
    inputs: list,
    practices: list,
    products: list,
    emissions: list
):
    cycle = cycle | {
        'site': site,
        'completeness': completeness,
        'inputs': non_empty_list(map(_format_aggregate(new_input), inputs)),
        'practices': cycle.get('practices', []) +
        cleanup_blank_nodes(map(_format_aggregate(new_practice, _filter_practice), practices)),
        'products': non_empty_list(map(_format_aggregate(new_product), products))
    }
    # aggregate emissions after as it needs inputs and products
    cycle['emissions'] = non_empty_list(map(_format_aggregate(new_emission(cycle)), emissions))

    # set the primary product
    primary_product = (find_primary_product(cycle) or {}).get('term', {})
    product_id = primary_product.get('@id')
    if product_id:
        product = find_term_match(cycle.get('products'), product_id)
        product['primary'] = True
        # handle situation where product was not added, like all incomplete
        return cycle if product.get('term', {}).get('@id') == product_id else {}
    return {}


def format_terms_results(data: dict):
    inputs = data.get('inputs', [])
    practices = data.get('practices', [])
    products = data.get('products', [])
    emissions = data.get('emissions', [])
    ids = data.get('node-ids', [])
    if len(ids) > 0:
        cycle = _format_results(
            cycle=_create_cycle(),
            site=data.get('site'),
            completeness=completeness_from_count(data.get('completeness-count', {})),
            inputs=inputs,
            practices=practices,
            products=products,
            emissions=emissions
        )
        return cycle | {
            'practices': cycle.get('practices', []) + (
                [_aggregated_version(organic_practice())] if data.get('organic') or is_organic(cycle) else []
            ),
            'aggregatedCycles': format_aggregated_list('Cycle', data.get('node-ids', [])),
            'aggregatedSources': format_aggregated_list('Source', data.get('source-ids', [])),
            'numberOfCycles': data.get('numberOfCycles')
        } if cycle else None
    return None


def format_country_results(data: dict, site: dict):
    inputs = data.get('inputs', [])
    practices = data.get('practices', [])
    products = data.get('products', [])
    emissions = data.get('emissions', [])
    cycles = data.get('nodes', [])
    if len(cycles) > 0:
        first_cycle = cycles[0]
        primary_product = {'term': data.get('product')}
        cycle = _create_cycle(pick(first_cycle, ['startDate', 'endDate']))
        completeness = aggregate_completeness(data.get('node-completeness', []))
        return {
            'name': _cycle_name(cycle, primary_product, False, False, False),
            'id': _cycle_id(cycle, primary_product, False, False, False),
            **_format_results(cycle, site, completeness, inputs, practices, products, emissions),
            'aggregatedCycles': format_aggregated_list('Cycle', cycles),
            'aggregatedSources': (
                format_aggregated_list('Source', cycles) or format_aggregated_sources(cycles, 'defaultSource')
            ),
            'numberOfCycles': data.get('numberOfCycles'),
        }
    return None


def _sum_blank_nodes(blank_nodes: list):
    values = flatten([n.get('value', []) for n in blank_nodes])
    value = (
        list_sum(values) if all(map(is_number, values)) else all(values)
    ) if values else None
    return {
        **blank_nodes[0],
        'value': non_empty_list([value]),
        # needed for background emissions
        'inputs': flatten([n.get('inputs', []) for n in blank_nodes])
    }


def _group_blank_nodes(product: dict, product_value: float, cycle: dict, list_key: str):
    # for non-crop products, normalize all the data back to 1 product
    normalize = product.get('term', {}).get('termType') != TermTermType.CROP.value
    items = list(map(_sum_blank_nodes, reduce(group_by_term_id(), cycle.get(list_key, []), {}).values()))
    return [
        item | {
            'value': [
                (v / (product_value if product_value else 1)) if is_number(v) else v for v in item.get('value', [])
            ]
        } for item in items
    ] if normalize else items


def _should_include_cycle(cycle: dict):
    should_include = all([
        # skip any cycle that does not represent a commercial practice
        cycle.get('commercialPracticeTreatment', True)
    ])
    if not should_include:
        logger.debug('Cycle %s skipped because commercialPracticeTreatment=true.', cycle.get('@id'))
    return should_include


def format_for_grouping(cycles: list) -> list:
    def format(cycle: dict):
        product = find_primary_product(cycle) or {}
        site = cycle.get('site')
        product_value = list_sum(flatten([
            # account for every product with the same `@id`
            p.get('value', []) for p in cycle.get('products', [])
            if p.get('term', {}).get('@id') == product.get('term', {}).get('@id')
        ]), 0)
        return cycle | {
            'inputs': _group_blank_nodes(product, product_value, cycle, 'inputs'),
            'practices': _group_blank_nodes(product, product_value, cycle, 'practices'),
            'products': _group_blank_nodes(product, product_value, cycle, 'products'),
            'emissions': _group_blank_nodes(product, product_value, cycle, 'emissions'),
            'site-id': site.get('@id'),
            'source-id': cycle.get('defaultSource', {}).get('@id'),
            'product': product.get('term'),
            'yield': product_value,
            'country': site.get('country'),
            'organic': is_organic(cycle),
            'irrigated': is_irrigated(cycle),
            'functionalUnit': cycle.get('functionalUnit'),
        } if _should_include_cycle(cycle) else None
    return non_empty_list(map(format, cycles))


def _cycle_id(n: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    return '-'.join(non_empty_list([
        primary_product.get('term', {}).get('@id'),
        _format_country_name(n.get('site', {}).get('country', {}).get('name')),
        _format_organic(organic) if include_matrix else '',
        _format_irrigated(irrigated) if include_matrix else '',
        n.get('startDate'),
        n.get('endDate'),
        _timestamp()
    ]))


def _cycle_name(cycle: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    return ' - '.join(non_empty_list([
        primary_product.get('term', {}).get('name'),
        cycle.get('site', {}).get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if organic else 'Conventional') if include_matrix else '',
            ('Irrigated' if irrigated else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([cycle.get('startDate'), cycle.get('endDate')])
    ]))


def _create_cycle(data: dict = {}):
    cycle = {'type': SchemaType.CYCLE.value} | data
    cycle['startDateDefinition'] = CycleStartDateDefinition.START_OF_YEAR.value
    cycle['dataPrivate'] = False
    cycle['defaultMethodClassification'] = CycleDefaultMethodClassification.MODELLED.value
    cycle['defaultMethodClassificationDescription'] = 'aggregated data'
    cycle['aggregatedDataValidated'] = False
    return _aggregated_node(cycle)


def update_cycle(country: dict, start: int, end: int, source: dict, functional_unit: str, include_matrix=True):
    def update(cycle: dict):
        cycle['startDate'] = str(start)
        cycle['endDate'] = str(end)
        cycle['functionalUnit'] = functional_unit
        cycle['site'] = update_site(country, source, False)(cycle['site'])
        primary_product = find_primary_product(cycle)
        organic = is_organic(cycle)
        irrigated = is_irrigated(cycle)
        cycle['name'] = _cycle_name(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['name'] = cycle['name']
        cycle['id'] = _cycle_id(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['id'] = cycle['id']
        return cycle if source is None else cycle | {'defaultSource': source}
    return update
