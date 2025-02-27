from hestia_earth.schema import MeasurementJSONLD, MeasurementStatsDefinition, MeasurementMethodClassification
from hestia_earth.utils.model import linked_node

from . import _set_dict_array, _set_dict_single


def new_measurement(data: dict):
    measurement = MeasurementJSONLD().to_dict()
    measurement['term'] = linked_node(data.get('term'))
    measurement['methodClassification'] = MeasurementMethodClassification.COUNTRY_LEVEL_STATISTICAL_DATA.value

    value = data.get('value')
    if value is not None:
        measurement['value'] = [value]
        measurement['statsDefinition'] = MeasurementStatsDefinition.SITES.value

    _set_dict_array(measurement, 'observations', data.get('observations'))
    _set_dict_array(measurement, 'min', data.get('min'))
    _set_dict_array(measurement, 'max', data.get('max'))
    _set_dict_array(measurement, 'sd', data.get('sd'), True)

    _set_dict_single(measurement, 'startDate', data.get('startDate'))
    _set_dict_single(measurement, 'endDate', data.get('endDate'))

    if data.get('depthUpper') is not None:
        measurement['depthUpper'] = int(data.get('depthUpper'))
    if data.get('depthLower') is not None:
        measurement['depthLower'] = int(data.get('depthLower'))

    return measurement
