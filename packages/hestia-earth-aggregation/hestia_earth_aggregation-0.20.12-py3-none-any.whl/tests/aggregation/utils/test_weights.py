from hestia_earth.aggregation.utils.weights import _country_irrigated_weight


def test_irrigated_weight():
    country_id = 'GADM-ECU'
    assert _country_irrigated_weight(country_id, 2019) == 0.06885166693509422
