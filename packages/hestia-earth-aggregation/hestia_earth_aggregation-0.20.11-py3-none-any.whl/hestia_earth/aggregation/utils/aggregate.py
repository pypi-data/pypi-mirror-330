from typing import List
from functools import reduce
from hestia_earth.utils.tools import non_empty_list, flatten

from . import weighted_average, _min, _max, _sd, pick
from .emission import get_method_tier


def _aggregate(blank_nodes: list, combine_values: bool):
    first_node = blank_nodes[0]
    term = first_node.get('term')

    economicValueShare_values = non_empty_list(flatten(map(lambda v: v.get('economicValueShare', []), blank_nodes)))
    economicValueShare = weighted_average([(v, 1) for v in economicValueShare_values])

    all_values = non_empty_list(flatten(map(lambda v: v.get('value', []), blank_nodes)))
    value = weighted_average([(v, 1) for v in all_values])

    max_value = _max(all_values) if not combine_values else _max(non_empty_list(flatten([
        n.get('max', []) for n in blank_nodes
    ] + all_values)), min_observations=len(all_values) or 1)
    min_value = _min(all_values) if not combine_values else _min(non_empty_list(flatten([
        n.get('min', []) for n in blank_nodes
    ] + all_values)), min_observations=len(all_values) or 1)
    observations = len(all_values) if not combine_values else sum(non_empty_list(flatten([
        n.get('observations', 1) for n in blank_nodes
    ])))

    inputs = flatten([n.get('inputs', []) for n in blank_nodes])
    methodTier = get_method_tier(blank_nodes)

    return {
        'term': term,
        'economicValueShare': economicValueShare,
        'value': value,
        'max': max_value,
        'min': min_value,
        'sd': _sd(all_values),
        'observations': observations,
        'inputs': inputs,
        'methodTier': methodTier
    } | pick(first_node, ['depthUpper', 'depthLower', 'startDate', 'endDate']) if len(all_values) > 0 else None


def _aggregate_term(aggregates_map: dict, combine_values: bool):
    def aggregate(term_id: str):
        blank_nodes = aggregates_map.get(term_id, [])
        return _aggregate(blank_nodes, combine_values) if len(blank_nodes) > 0 else None
    return aggregate


def aggregate(aggregate_keys: List[str], data: dict, combine_values: bool = False) -> dict:
    def aggregate_single(key: str):
        aggregates_map: dict = data.get(key)
        terms = aggregates_map.keys()
        return non_empty_list(map(_aggregate_term(aggregates_map, combine_values), terms))

    return reduce(lambda prev, curr: prev | {curr: aggregate_single(curr)}, aggregate_keys, data)
