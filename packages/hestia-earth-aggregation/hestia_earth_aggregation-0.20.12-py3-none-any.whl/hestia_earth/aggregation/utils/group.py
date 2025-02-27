from functools import reduce
from hestia_earth.utils.tools import safe_parse_date, non_empty_list, flatten

from . import pick, sum_data
from .completeness import blank_node_completeness_key, is_complete, combine_completeness_count
from .practice import filter_practices
from .blank_node import filter_blank_nodes, filter_aggregate
from .management import filter_management


def _end_date_year(node: dict):
    date = safe_parse_date(node.get('endDate'))
    return date.year if date else None


_FILTER_BLANK_NODES = {
    'measurements': filter_blank_nodes,
    # filtering by date is done over start-20 to end years
    'management': lambda blank_nodes, start_year, end_year: filter_blank_nodes(
        filter_management(blank_nodes, start_year, end_year)
    ),
    'practices': lambda blank_nodes, start_year, end_year: filter_blank_nodes(
        filter_practices(blank_nodes),
        start_year,
        end_year
    ),
    'emissions': lambda blank_nodes, *args: list(filter(filter_aggregate, blank_nodes))
}


def _filter_blank_nodes(node: dict, list_key: str, start_year: int, end_year: int):
    blank_nodes = node.get(list_key, [])
    blank_nodes = _FILTER_BLANK_NODES.get(list_key, lambda values, *args: values)(blank_nodes, start_year, end_year)
    # make sure we skip any blank node marked as `deleted`
    return [n for n in blank_nodes if not n.get('deleted')]


DATA_GROUP_KEYS = ['organic', 'irrigated', 'country', 'product', 'functionalUnit', 'siteType']
GROUP_BY_EXTRA_VALUES = {
    'measurements': lambda node: [
        node.get('startDate'), node.get('endDate'),
        node.get('depthUpper'), node.get('depthLower')
    ],
    'management': lambda node: [node.get('startDate'), node.get('endDate')],
}


def group_by_term_id(list_key: str = None):
    def group_by(group: dict, node: dict):
        keys = [node.get('term', {}).get('@id')] + GROUP_BY_EXTRA_VALUES.get(list_key, lambda *args: [])(node)
        keys = list(map(str, non_empty_list(keys)))
        group_key = '-'.join(keys)
        if group_key not in group:
            group[group_key] = []
        group[group_key].append(node)
        return group
    return group_by


def group_blank_nodes(
    nodes: list,
    props: list,
    start_year: int = None,
    end_year: int = None,
    product: dict = None,
    include_completeness: bool = True
) -> dict:
    completeness = non_empty_list([node.get('completeness') for node in nodes])
    completeness_count = combine_completeness_count(completeness)

    group = {
        'nodes': [],
        'node-completeness': completeness if include_completeness else None,
        'completeness-count': completeness_count,
        'node-ids': [],
        'source-ids': [],
        'site-ids': []
    } | {prop: {} for prop in props}

    def group_by(group: dict, node: dict):
        data = pick(node, DATA_GROUP_KEYS) | {'year': _end_date_year(node)}
        group['nodes'].append(pick(node, [
            '@id', 'id', 'startDate', 'endDate',
            'numberOfCycles', 'numberOfSites',
            'aggregatedCycles', 'aggregatedSites', 'aggregatedSources'
        ]) | data)

        node_id = node.get('@id', node.get('id'))
        group['node-ids'].append(node_id)
        group['site-ids'].extend(non_empty_list([node.get('site-id')]))
        group['source-ids'].extend(non_empty_list([node.get('source-id') or node.get('defaultSource', {}).get('@id')]))

        def group_by_prop(list_key: str):
            values = flatten(map(
                lambda v: v | data | {
                    'completeness': is_complete(node, product, v),
                    'completeness-key': blank_node_completeness_key(v, product)
                } | {'id': node_id}, _filter_blank_nodes(node, list_key, start_year, end_year)))
            return reduce(group_by_term_id(list_key), values, group[list_key])

        group = reduce(lambda prev, curr: prev | {curr: group_by_prop(curr)}, props, group)
        return group | data

    data = reduce(group_by, nodes, group)

    return data | {
        'numberOfCycles': sum_data(nodes, 'numberOfCycles'),
        'numberOfSites': sum_data(nodes, 'numberOfSites')
    }
