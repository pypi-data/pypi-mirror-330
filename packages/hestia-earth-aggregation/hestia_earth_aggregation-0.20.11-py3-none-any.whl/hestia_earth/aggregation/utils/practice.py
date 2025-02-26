from hestia_earth.schema import TermTermType, SchemaType, PracticeStatsDefinition
from hestia_earth.utils.model import filter_list_term_type, linked_node
from hestia_earth.utils.tools import flatten
from hestia_earth.utils.api import download_hestia


def new_practice(data):
    node = {'@type': SchemaType.PRACTICE.value}
    term = data.get('term') if isinstance(data, dict) else download_hestia(data)
    node['term'] = linked_node(term)
    value = data.get('value')
    if value is not None:
        node['value'] = [round(value, 8)]
        node['statsDefinition'] = PracticeStatsDefinition.CYCLES.value
    return node


def organic_practice():
    node = {'@type': SchemaType.PRACTICE.value}
    node['term'] = linked_node(download_hestia('organic'))
    node['value'] = [100]
    node['statsDefinition'] = PracticeStatsDefinition.CYCLES.value
    return node


_PRACTICE_AGGREGATE_BY_UNITS = {
    TermTermType.LANDUSEMANAGEMENT: ['ratio', 'number', 'days']
}
_PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES = [
    t.value
    for t in TermTermType
    if t not in _PRACTICE_AGGREGATE_BY_UNITS
]


def filter_practices(practices: list):
    return filter_list_term_type(practices, _PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES) + flatten([
        p
        for term_type, units in _PRACTICE_AGGREGATE_BY_UNITS.items()
        for p in filter_list_term_type(practices, term_type)
        if p.get('term', {}).get('units') in units
    ])
