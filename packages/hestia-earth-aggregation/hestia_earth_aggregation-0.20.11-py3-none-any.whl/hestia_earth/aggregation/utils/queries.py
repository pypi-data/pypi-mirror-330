import os
import json
import math
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import NodeType, TermTermType, SiteSiteType
from hestia_earth.utils.api import download_hestia, search, _safe_post_request
from hestia_earth.utils.tools import non_empty_list
from hestia_earth.utils.request import api_url
from hestia_earth.utils.storage._s3_client import _get_s3_client, _get_bucket

from hestia_earth.aggregation.log import logger
from . import HestiaError, _save_json, pick
from .term import DEFAULT_COUNTRY_NAME, _format_country_name, _fetch_countries, _is_global

SEARCH_LIMIT = 10000
_MATCH_AGGREGATED_QUERY = {'match': {'aggregated': 'true'}}
_MATCH_AGGREGATED_VALIDATED_QUERY = {'match': {'aggregatedDataValidated': 'true'}}
# aggregate every 20 years
TIME_PERIOD = 20


def _current_date(): return datetime.now().date().strftime('%Y-%m-%d')


def _date_range_query(start: int, end: int):
    return {'range': {'endDate': {'gte': str(start), 'lte': str(end)}}} if start and end else None


def _product_query(product_name: str = None, match_aggregated=False):
    return {
        'bool': {
            'must': non_empty_list([
                {'match': {'@type': NodeType.CYCLE.value}},
                {
                    'nested': {
                        'path': 'products',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'products.term.name.keyword': product_name}},
                                    {'match': {'products.primary': 'true'}}
                                ]
                            }
                        }
                    }
                } if product_name else None,
                _MATCH_AGGREGATED_QUERY if match_aggregated else None
            ]),
            'must_not': non_empty_list([
                None if match_aggregated else _MATCH_AGGREGATED_QUERY
            ])
        }
    }


COUNTRY_FIELD_BY_TYPE = {
    NodeType.CYCLE.value: 'site.country'
}


def _country_query(country_name: str):
    return {'match': {'site.country.name.keyword': country_name}}


# restrict siteTypes that we aggregate
_animal_site_types = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.ANIMAL_HOUSING.value,
]
SITE_TYPE_MAPPING = {
    TermTermType.CROP.value: [
        SiteSiteType.CROPLAND.value,
        SiteSiteType.GLASS_OR_HIGH_ACCESSIBLE_COVER.value
    ],
    TermTermType.LIVEANIMAL.value: _animal_site_types,
    TermTermType.ANIMALPRODUCT.value: _animal_site_types,
    TermTermType.LIVEAQUATICSPECIES.value: [
        SiteSiteType.POND.value,
        SiteSiteType.RIVER_OR_STREAM.value,
        SiteSiteType.LAKE.value,
        SiteSiteType.SEA_OR_OCEAN.value
    ],
    TermTermType.PROCESSEDFOOD.value: [
        SiteSiteType.AGRI_FOOD_PROCESSOR.value
    ]
}


def _site_type_query(product: dict):
    site_types = SITE_TYPE_MAPPING.get(product.get('termType'), [])
    return {
        'bool': {
            'should': [{'match': {'site.siteType.keyword': site_type}} for site_type in site_types],
            'minimum_should_match': 1
        }
    }


def _exec_paginated_search(query: str, fields: list, search_after=None):
    index = os.getenv('ELASTICSEARCH_INDEX', 'hestia-data')
    url = f"{os.getenv('ELASTICSEARCH_URL')}/{index}/_search"
    data = {
        "size": SEARCH_LIMIT,
        "query": query,
        "_source": {"includes": fields},
        "sort": [{"@id.keyword": "asc"}]
    } | ({
        "search_after": search_after
    } if search_after else {})
    # note: set `, verify=False` to search on localhost tunnel
    response = requests.post(url, json.dumps(data), headers={'Content-Type': 'application/json'})
    results = response.json().get('hits', {}).get('hits', [])
    last_hit_search_after = results[-1].get('sort') if results else None
    return [r.get('_source') for r in results] + (
        _exec_paginated_search(query, fields, last_hit_search_after) if last_hit_search_after else []
    )


def _paginate_search(query: str, fields: list):
    try:
        return _exec_paginated_search(query, fields)
    except Exception as e:
        logger.warning('Error when paginating search:', str(e))
        return search(query=query, limit=SEARCH_LIMIT, fields=fields)


def _download_by_state(node: dict, data_state: str):
    try:
        node = download_hestia(node.get('@id'), node.get('@type'), data_state=data_state)
        return node if node.get('@type') else None
    except Exception:
        logger.debug('skip non-%s %s: %s', data_state, node.get('@type'), node.get('@id'))
        return None


def _download_recalculated_node(node: dict, data_state: str):
    key = '/'.join([data_state, node.get('@type'), f"{node.get('@id')}.jsonld"])

    # try to download from S3 and make sure last stage is reached, otherwise skip
    try:
        content = _get_s3_client().get_object(Bucket=_get_bucket(), Key=key)
        metadata = content.get('Metadata', {})
        is_max_stage = metadata.get('stage', 1) == metadata.get('maxstage', 1)
        body = content.get('Body')
        return json.loads(body.read()) if is_max_stage and body else None
    except ImportError:
        return _download_by_state(node, data_state)


def download_node(node: dict):
    try:
        data_state = (
            # no stage for aggregated node as only IA is recalculated
            'recalculated' if node.get('@type') in [NodeType.IMPACTASSESSMENT.value] else 'original'
        ) if node.get('aggregated', False) else 'recalculated'
        download_function = _download_recalculated_node if data_state == 'recalculated' else _download_by_state
        return download_function(node, data_state)
    except Exception as e:
        raise HestiaError('An error occurred while downloading the node', {
            'node': pick(node, ['@type', '@id']),
            'error': str(e)
        })


def download_site(site: dict):
    # aggregated site will not have a recalculated version
    data = download_node(site)
    if not data:
        raise HestiaError(f"Failed to download Site with id {site.get('@id')}")
    _save_json(data, f"{data.get('@type')}/{data.get('@id')}")
    return data if data.get('@type') else None


def _safe_download_node(node: dict):
    try:
        data = download_node(node)
        return {
            'node': pick(node, ['@type', '@id']),
            'data': data
        }
    except HestiaError as e:
        return {
            'node': pick(node, ['@type', '@id']),
            'error': e.error.get('error')
        }


def download_nodes(nodes: list):
    total = len(nodes)
    with ThreadPoolExecutor() as executor:
        results = non_empty_list(executor.map(_safe_download_node, nodes))
    error_nodes = non_empty_list([v for v in results if v.get('error')])
    existing_nodes = non_empty_list([v.get('data') for v in results])
    logger.debug('downloaded %s nodes / %s total nodes', str(len(existing_nodes)), str(total))
    if error_nodes:
        raise HestiaError('Failed to download nodes', {'errors': error_nodes})
    return existing_nodes


def _country_nodes_query(product: dict, start_year: int, end_year: int, country: str):
    query = _product_query(product.get('name'))
    date_range = _date_range_query(start_year, end_year)
    query['bool']['must'].extend([date_range] if date_range else [])
    query['bool']['must'].append(_site_type_query(product))
    if country.get('name') != DEFAULT_COUNTRY_NAME:
        query['bool']['must'].append(_country_query(country.get('name')))

    return query


def find_country_nodes(product: dict, start_year: int, end_year: int, country: dict):
    """
    Find all Cycles with the same primary `product`, `country` and `endDate` between start and end years.
    Note: this function only returns the `@type` and `@id` fields for each Cycle.
    """
    nodes = _paginate_search(
        query=_country_nodes_query(product, start_year, end_year, country),
        fields=['@id', '@type']
    )
    return nodes


def _global_query(product_name: str, start_year: int, end_year: int):
    countries = _fetch_countries()
    query = {
        'bool': {
            'must': non_empty_list([
                _product_query(product_name, match_aggregated=True),
                _MATCH_AGGREGATED_QUERY,
                _MATCH_AGGREGATED_VALIDATED_QUERY,
                _date_range_query(start_year, end_year)
            ]),
            'must_not': [
                # do not include lower levels of country breakdown
                {'match': {'name': 'Conventional'}},
                {'match': {'name': 'Irrigated'}},
                {'match': {'name': 'Organic'}}
            ],
            'should': [
                _country_query(country.get('name')) for country in countries
            ],
            'minimum_should_match': 1
        }
    }
    return query


def _global_nodes(product_name: str, start_year: int, end_year: int):
    nodes = _paginate_search(
        query=_global_query(product_name, start_year, end_year),
        fields=['@id', '@type', 'aggregated']
    )
    return download_nodes(nodes)


def _sub_country_nodes(product: dict, start_year: int, end_year: int, region_name: str):
    query = {
        'bool': {
            'must': [
                {'match': {'@type': NodeType.TERM.value}},
                {'match': {'termType': TermTermType.REGION.value}},
                {'match': {'subClassOf.name.keyword': region_name}}
            ]
        }
    }
    sub_regions = _paginate_search(query=query, fields=['@id', 'name'])
    nodes = [{
        '@type': NodeType.CYCLE.value,
        '@id': '-'.join([
            product.get('@id'),
            _format_country_name(v['name']),
            str(start_year),
            str(end_year)
        ]),
        'aggregated': True
    } for v in sub_regions]
    return download_nodes(nodes)


def find_global_nodes(product: dict, start_year: int, end_year: int, country: dict):
    product_name = product.get('name')
    country_name = country.get('name')
    nodes = _sub_country_nodes(
        product, start_year, end_year, country_name
    ) if country_name != DEFAULT_COUNTRY_NAME else _global_nodes(
        product_name, start_year, end_year
    )
    _save_json({'nodes': nodes}, '-'.join([
        str(v) for v in ['nodes', product_name, country_name, start_year, end_year] if v
    ]))
    return nodes


def count_nodes(product: dict, start_year: int, end_year: int, country: dict):
    """
    Return the number of Nodes that will be used to aggregate.
    """
    product_name = product.get('name')
    country_name = country.get('name')
    query = (
        -1 if _is_global(country) else _country_nodes_query(product, start_year, end_year, country)
    ) if country_name != DEFAULT_COUNTRY_NAME else _global_query(product_name, start_year, end_year)
    return _safe_post_request(f"{api_url()}/count", {'query': query})


def _get_time_ranges(earliest_date: str, latest_date: str, period_length: int = TIME_PERIOD):
    """
    Get time ranges starting from the earliest date to today.

    Parameters
    ----------
    earliest_date : str
        The start date of the time range.
    latest_date : str
        The end date of the time range.
    period_length : int
        Optional - length of the period, 20 by default.

    Returns
    -------
    list
        A list of time periods.
        Example: `[(1990, 2009), (2010, 2024)]`
    """
    earliest_year = int(earliest_date[0:4])
    latest_year = int(latest_date[0:4])

    # start from the minimum century - 10 years. Go every X years. Filter for dates that contain min/max
    min_year = round(math.floor(earliest_year / 100) * 100) - 10
    max_year = int(_current_date()[:4])
    periods = [(i, min(i+period_length-1, max_year)) for i in range(min_year, max_year, period_length)]
    return [(start, end) for (start, end) in periods if any([
        start <= earliest_year <= end,
        earliest_year <= start and end <= latest_year,
        start <= latest_year <= end
    ])]


def _earliest_date(product_name: str, country: dict):
    is_global = _is_global(country)
    query = _product_query(product_name, match_aggregated=is_global)
    if not is_global:
        query['bool']['must'].append(_country_query(country.get('name')))
    results = search(query, limit=1, fields=['endDate'], sort=[{'endDate.keyword': 'asc'}])
    return results[0].get('endDate') if len(results) > 0 else None


def _latest_date(product_name: str, country: dict):
    is_global = _is_global(country)
    query = _product_query(product_name, match_aggregated=is_global)
    if not is_global:
        query['bool']['must'].append(_country_query(country.get('name')))
    results = search(query, limit=1, fields=['endDate'], sort=[{'endDate.keyword': 'desc'}])
    return results[0].get('endDate') if len(results) > 0 else None


def get_time_ranges(country: dict, product_name: str):
    from_date = _earliest_date(product_name, country)
    to_date = _latest_date(product_name, country) if from_date else None
    return _get_time_ranges(from_date, to_date) if to_date else []
