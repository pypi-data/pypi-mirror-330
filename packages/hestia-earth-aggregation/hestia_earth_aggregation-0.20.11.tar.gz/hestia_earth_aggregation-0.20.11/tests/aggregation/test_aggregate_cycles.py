import os
import json
import pytest
from unittest.mock import Mock, patch
from hestia_earth.utils.model import find_primary_product

from tests.utils import (
    fixtures_path, start_year, end_year, current_date, SOURCE, WORLD,
    overwrite_expected, order_results, fake_aggregated_version, fake_download
)
from hestia_earth.aggregation.aggregate_cycles import run_aggregate

class_path = 'hestia_earth.aggregation.aggregate_cycles'
fixtures_folder = os.path.join(fixtures_path, 'cycle')

_files = [
    f for f in os.listdir(fixtures_folder)
    if os.path.isfile(os.path.join(fixtures_folder, f)) and f.endswith('.jsonld')
]


def _node_id(node: dict): return node.get('@id') or node.get('id')


def fake_download_site(cycles: list):
    def download(site: dict):
        return next((c.get('site') for c in cycles if _node_id(c.get('site')) == _node_id(site)), None)
    return download


@pytest.mark.parametrize('filename', _files)
@patch('hestia_earth.aggregation.utils.cycle._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.cycle._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.practice.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.queries.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.term.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.management._current_date', return_value=current_date)
@patch('hestia_earth.aggregation.utils.queries._current_date', return_value=current_date)
@patch('hestia_earth.aggregation.utils.cycle._timestamp', return_value='')
@patch('hestia_earth.aggregation.utils.aggregate_country_nodes.download_site')
@patch('hestia_earth.aggregation.utils.aggregate_country_nodes.download_nodes')
@patch(f"{class_path}.find_country_nodes")
def test_aggregate_country(
    mock_find_nodes: Mock,
    mock_download_nodes: Mock,
    mock_download_site: Mock,
    mock_1: Mock,
    mock_2: Mock,
    mock_3: Mock,
    mock_4: Mock,
    mock_5: Mock,
    mock_6: Mock,
    mock_7: Mock,
    mock_8: Mock,
    mock_9: Mock,
    mock_10: Mock,
    filename: str
):
    filepath = os.path.join(fixtures_folder, filename)
    with open(filepath, encoding='utf-8') as f:
        cycles = json.load(f)

    mock_find_nodes.return_value = [{'@id': c.get('@id')} for c in cycles]
    mock_download_site.side_effect = fake_download_site(cycles)

    def fake_download_nodes(nodes: list):
        ids = [n.get('@id') for n in nodes]
        return [c for c in cycles if c.get('@id') in ids]

    mock_download_nodes.side_effect = fake_download_nodes

    expected_filepath = os.path.join(fixtures_folder, 'country', filename)
    with open(expected_filepath, encoding='utf-8') as f:
        expected = json.load(f)

    product = find_primary_product(cycles[0])['term']
    country = cycles[0]['site']['country']

    results = run_aggregate(
        country=country,
        product=product,
        start_year=start_year,
        end_year=end_year,
        source=SOURCE
    )
    overwrite_expected(expected_filepath, results)
    assert order_results(results) == expected


@pytest.mark.parametrize('filename', _files)
@patch('hestia_earth.aggregation.utils.cycle._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.cycle._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.practice.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.queries.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.term.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.utils.management._current_date', return_value=current_date)
@patch('hestia_earth.aggregation.utils.queries._current_date', return_value=current_date)
@patch('hestia_earth.aggregation.utils.cycle._timestamp', return_value='')
@patch(f"{class_path}.download_site")
@patch(f"{class_path}.find_global_nodes")
def test_aggregate_global(
    mock_find_nodes: Mock,
    mock_download_site: Mock,
    mock_1: Mock,
    mock_2: Mock,
    mock_3: Mock,
    mock_4: Mock,
    mock_5: Mock,
    mock_6: Mock,
    mock_7: Mock,
    mock_8: Mock,
    mock_9: Mock,
    mock_10: Mock,
    filename: str
):
    filepath = os.path.join(fixtures_folder, 'country', filename)
    with open(filepath, encoding='utf-8') as f:
        cycles = json.load(f)

    mock_find_nodes.return_value = cycles
    mock_download_site.side_effect = fake_download_site(cycles)

    expected_filepath = os.path.join(fixtures_folder, 'global', filename)
    with open(expected_filepath, encoding='utf-8') as f:
        expected = json.load(f)

    product = find_primary_product(cycles[0])['term']

    results = run_aggregate(
        country=WORLD,
        product=product,
        start_year=start_year,
        end_year=end_year,
        source=SOURCE
    )
    overwrite_expected(expected_filepath, results)
    assert order_results(results) == expected
