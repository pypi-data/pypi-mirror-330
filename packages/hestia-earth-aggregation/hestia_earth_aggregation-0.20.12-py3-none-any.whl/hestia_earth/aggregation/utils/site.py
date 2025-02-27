from hestia_earth.schema import SchemaType, SiteDefaultMethodClassification
from hestia_earth.utils.tools import non_empty_list

from . import SITE_AGGREGATION_KEYS, _aggregated_node, sum_data, _aggregated_version, format_aggregated_list
from .aggregate import aggregate
from .term import _format_country_name, update_country
from .blank_node import cleanup_blank_nodes
from .source import format_aggregated_sources
from .group import group_blank_nodes
from .measurement import new_measurement
from .management import new_management


def _format_aggregate(new_func: dict):
    def format(aggregate: dict):
        return _aggregated_version(new_func(aggregate))
    return format


def format_site_results(data: dict):
    measurements = data.get('measurements', [])
    management = data.get('management', [])
    return ({
        'measurements': cleanup_blank_nodes(map(_format_aggregate(new_measurement), measurements)),
    } if measurements else {}) | ({
        'management': cleanup_blank_nodes(map(_format_aggregate(new_management), management))
    } if management else {})


def aggregate_sites_data(data: dict, combine_values: bool = False, sites: list = []):
    aggregates = aggregate(SITE_AGGREGATION_KEYS, data, combine_values=combine_values)
    sites = sites or [data]
    return create_site(sites[0]) | format_site_results(aggregates) | {
        'aggregatedSites': format_aggregated_list('Site', sites),
        'aggregatedSources': format_aggregated_sources(sites, 'defaultSource'),
        'numberOfSites': sum_data(sites, 'numberOfSites')
    }


def aggregate_sites(sites: list):
    data = group_blank_nodes(nodes=sites, props=SITE_AGGREGATION_KEYS)
    return aggregate_sites_data(data=data, combine_values=True, sites=sites)


def _site_id(n: dict, include_siteType: bool):
    return '-'.join(non_empty_list([
        _format_country_name(n.get('country', {}).get('name')),
        n.get('siteType') if include_siteType else None
    ]))


def _site_name(n: dict, include_siteType: bool):
    return ' - '.join(non_empty_list([
        n.get('country', {}).get('name'),
        n.get('siteType') if include_siteType else None
    ]))


def create_site(data: dict, include_siteType=True):
    site = {'type': SchemaType.SITE.value}
    site['country'] = data['country']
    site['siteType'] = data['siteType']
    site['name'] = _site_name(data, include_siteType)
    site['id'] = _site_id(data, include_siteType)
    site['defaultMethodClassification'] = SiteDefaultMethodClassification.MODELLED.value
    site['defaultMethodClassificationDescription'] = 'aggregated data'
    site['dataPrivate'] = False
    site['aggregatedDataValidated'] = False
    return _aggregated_node(site)


def update_site(country: str, source: dict = None, include_siteType=True):
    def update(site: dict):
        site['country'] = update_country(country or site.get('country'))
        site['name'] = _site_name(site, include_siteType)
        site['id'] = _site_id(site, include_siteType)
        return site | ({} if source is None else {'defaultSource': source})
    return update
