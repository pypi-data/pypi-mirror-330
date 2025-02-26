from typing import List
from functools import reduce
from hestia_earth.schema import SchemaType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list, flatten, list_sum, is_number, safe_parse_float
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.blank_node import get_node_value

from hestia_earth.aggregation.log import logger
from . import pick, match_dates, _min, _max
from .term import DRY_MATTER_TERM_ID, term_dryMatter, should_aggregate
from .management import aggregated_dates


def _formatDepth(depth: str):
    # handle float values
    return str(int(depth)) if is_number(depth) else ''


def default_missing_value(term: dict):
    # value can be string, number or boolean
    # use lookup `valueType` to determine which value to add
    lookup = download_lookup(f"{term.get('termType')}.csv")
    value_type = get_table_value(lookup, 'termid', term.get('@id'), column_name('valueType'))
    return {'boolean': False}.get(value_type, 0)


def _node_dryMatter(blank_node: dict):
    return safe_parse_float(find_term_match(blank_node.get('properties', []), DRY_MATTER_TERM_ID).get('value'))


def node_dryMatter_rescale_ratio(blank_node: dict):
    """
    Return the rescale ratio between the user provided `dryMatter` and HESTIA default `dryMatter`.
    """
    # for products with the `dryMatter` property, need to rescale using our default value
    node_dm = _node_dryMatter(blank_node)
    default_dm = term_dryMatter(blank_node.get('term', {})) if node_dm else 0
    return node_dm / default_dm if all([node_dm, default_dm]) else 1


def _blank_node_dates(blank_node: dict):
    return aggregated_dates(blank_node) if blank_node.get('@type') == SchemaType.MANAGEMENT.value else (
        pick(blank_node, ['startDate', 'endDate'])
    )


def _group_blank_nodes(nodes: list):
    """
    Group a list of blank nodes using:
    - `termType`
    - the `depthUpper` and `depthLower`
    - the `startDate` and `endDate`
    - the lookup group `sumMax100Group` or `sumIs100Group` or `booleanGroup` if specified

    Parameters
    ----------
    nodes : list
        List of blank nodes with their index.
    """
    def group_by(group: dict, blank_node: dict):
        term = blank_node.get('term', {})
        term_type = term.get('termType')
        lookup = download_lookup(f"{term_type}.csv")
        sum_below_100_group = get_table_value(lookup, 'termid', term.get('@id'), column_name('sumMax100Group')) \
            if lookup is not None else None
        sum_equal_100_group = get_table_value(lookup, 'termid', term.get('@id'), column_name('sumIs100Group')) \
            if lookup is not None else None
        boolean_group = get_table_value(lookup, 'termid', term.get('@id'), column_name('booleanGroup')) \
            if lookup is not None else None

        keys = non_empty_list([
            term_type,
            _formatDepth(blank_node.get('depthUpper')),
            _formatDepth(blank_node.get('depthLower')),
            blank_node.get('startDate'),
            blank_node.get('endDate'),
            sum_below_100_group,
            sum_equal_100_group,
            boolean_group
        ])
        key = '-'.join(keys)

        group[key] = group.get(key, []) + [{
            'key': key,
            'node': blank_node,
            'sumMax100Group': sum_below_100_group,
            'sumIs100Group': sum_equal_100_group,
            'booleanGroup': boolean_group
        }]

        return group

    return reduce(group_by, nodes, {})


def _filter_by_array_treatment(blank_node: dict):
    term = blank_node.get('term', {})
    lookup = download_lookup(f"{term.get('termType')}.csv")
    value = get_table_value(lookup, 'termid', term.get('@id'), column_name('arrayTreatmentLargerUnitOfTime'))
    # ignore any blank node with time-split data
    return not value


def _filter_needs_depth(blank_node: dict):
    term = blank_node.get('term', {})
    lookup = download_lookup(f"{term.get('termType')}.csv")
    needs_depth = get_table_value(lookup, 'termid', term.get('@id'), column_name('recommendAddingDepth'))
    return not needs_depth or all([blank_node.get('depthUpper') is not None, blank_node.get('depthLower') is not None])


def _missing_blank_node(node_type: str, term_type: str, term_id: str, units: str):
    term = {'@type': 'Term', 'termType': term_type, '@id': term_id, 'units': units}
    return {
        '@type': node_type,
        'term': term,
        'value': [default_missing_value(term)]
    }


def _add_missing_blank_nodes(blank_nodes: List[dict]):
    existing_ids = [v.get('node').get('term', {}).get('@id') for v in blank_nodes]
    group_id = blank_nodes[0].get('sumIs100Group')
    blank_node = blank_nodes[0].get('node')
    node_type = blank_node.get('@type')
    term = blank_node.get('term', {})
    term_type = term.get('termType')
    units = term.get('units')
    lookup = download_lookup(f"{term_type}.csv")
    term_ids = list(lookup[lookup[column_name('sumIs100Group')] == group_id].termid)
    missing_term_ids = [term_id for term_id in term_ids if term_id not in existing_ids]
    return [
        _missing_blank_node(node_type, term_type, term_id, units) | pick(blank_node, ['startDate', 'endDate'])
        for term_id in missing_term_ids
    ]


def _filter_grouped_nodes(blank_nodes: List[dict]):
    values = flatten([v.get('node').get('value', []) for v in blank_nodes])
    total_value = list_sum(values)
    blank_node = blank_nodes[0]
    sum_equal_100 = any([blank_node.get('sumMax100Group'), blank_node.get('sumIs100Group')])
    valid = not sum_equal_100 or 99.5 <= total_value <= 100.5
    if not valid and total_value > 0:
        logger.debug('Sum of group %s equal to %s, skipping.', blank_node.get('key'), total_value)
    # for every group that should be 100%, add all missing blank nodes in the same group with value=0
    dates = _blank_node_dates(blank_node.get('node'))
    results = [
        v.get('node') for v in blank_nodes
    ] + (
        _add_missing_blank_nodes(blank_nodes) if blank_node.get('sumIs100Group') else []
    ) if valid else []
    return [r | dates for r in results]


def node_type_allowed(term: dict, node_type: str):
    lookup = download_lookup(f"{term.get('termType')}.csv")
    values = get_table_value(lookup, 'termid', term.get('@id'), column_name('skipAggregatedNodeTypes'))
    skipped_values = values.split(';') if values and isinstance(values, str) else []
    return 'all' not in skipped_values and node_type not in skipped_values


def filter_aggregate(blank_node: dict):
    term = blank_node.get('term', {})
    return all([
        should_aggregate(term),
        node_type_allowed(term, blank_node.get('@type'))
    ])


def filter_blank_nodes(blank_nodes: List[dict], start_year: int = None, end_year: int = None):
    nodes = [v for v in blank_nodes if all([
        filter_aggregate(v),
        _filter_by_array_treatment(v),
        # _filter_needs_depth(v),  # allow measurements without depths to be aggregated together
        not start_year or not end_year or match_dates(v, start_year, end_year),
    ])]

    grouped_values = _group_blank_nodes(nodes)
    return flatten(map(_filter_grouped_nodes, grouped_values.values()))


def _is_value_zero(value):
    return value == [0] if isinstance(value, list) else (value == 0 or value == 0.0) if value is not None else False


def _remove_value_zero(blank_node: dict):
    term = blank_node.get('term', {})
    units = term.get('units')
    value = blank_node.get('value')
    term_type = term.get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    return all([
        units == '% area',
        _is_value_zero(value)
    ]) and bool(get_table_value(lookup, 'termid', term.get('@id'), column_name('sumIs100Group')))


def cleanup_blank_nodes(blank_nodes: List[dict]):
    # remove all blank nodes with `0` as value to reduce the node count
    return list(filter(lambda v: not _remove_value_zero(v), non_empty_list(blank_nodes)))


def _rescale_product_value_dm(node: dict, value: float):
    # for products with the `dryMatter` property, need to rescale using our default value
    rescale_ratio = node_dryMatter_rescale_ratio(node)
    return value * rescale_ratio


def _node_value(node: dict, key: str = 'value'):
    value = get_node_value(node, key, default=None)
    return _rescale_product_value_dm(node, value) if all([
        node.get('@type') == 'Product',
        key == 'value',
        value
    ]) else value


def _blank_node_value(blank_node: dict, complete: bool):
    """
    Handle completeness for `value` field.
    Rules:
    - if the blank_node is complete, use the value or set `0` if no value
    - if the blank_node is incomplete:
      - if it is the primary product, use the value
      - otherwise, do not use the value
    """
    default_value = default_missing_value(blank_node.get('term')) if complete else None
    value = get_node_value(blank_node, 'value', default=default_value)
    is_product = blank_node.get('@type') == 'Product'

    return (
        _rescale_product_value_dm(blank_node, value) if all([
            is_product,
            value
        ]) else value
    ) if complete is not False else (
        value if blank_node.get('primary') else None
    )


def _blank_node_evs(blank_node: dict, complete: bool):
    """
    Handle product evs.
    Only use the evs if the primary product is complete or has a value.
    """
    return blank_node.get('economicValueShare') if all([
        blank_node.get('primary'),
        complete or blank_node.get('value') is not None
    ]) else None


def map_blank_node(blank_node: dict):
    """
    Simplify blank node data by only keeping what we use in aggregation.
    """
    complete = blank_node.get('complete')
    value = _blank_node_value(blank_node, complete)
    return blank_node | {
        'value': value,
        'economicValueShare': _blank_node_evs(blank_node, complete),
        'min': _min(blank_node.get('min', []), min_observations=1),
        'max': _max(blank_node.get('max', []), min_observations=1),
        'observations': 0 if value is None else 1
    }
