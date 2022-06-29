#!/usr/bin/python3
from requests import Request
import geopandas as gpd
import re, json 

# load config dictionary from json file
with open('config.json') as f:
    config = json.load(f)

url = 'https://data.linz.govt.nz/services;key=' + config['my_linz_key'] + '/wfs?service=WFS&version=2.0.0'


def get_addresses_for_titles(titles):
    """
    Takes a list of title numbers and returns them with their addresses (zero to many per title)
    """
    title_address_dict = {}
    # first make wfs calls to get wkt geom for each title
    for title_no in titles:
        title_address_dict[title_no] = {}
        title_address_dict[title_no]['wkt_geom'] = get_title_wkt_geom(title_no)

    # then make a second call to get address for each wkt geom
    for title_no in titles:
        title_address_dict[title_no]['address'] = get_address_for_wkt_geom(title_address_dict[title_no]['wkt_geom'])
    return title_address_dict


def get_title_wkt_geom(title_no):
    """
    Takes a title number and returns the outline of that title as list of lat lon coordinates in wkt format
    """
    global url
    params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167', 'cql_filter': "title_no='" + title_no + "'", 'outputFormat': 'application/json'}
    url_plus_params = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(url_plus_params)
    # the data comes in lon lat order, which is not the format that WFS wants.  So we need to flip the order
    wkt_outline = re.sub(r'(\d+[.]\d+)\s+([-]\d+[.]\d+)', r'\2 \1',  str(data['geometry'][0])) 
    return wkt_outline


def get_address_for_wkt_geom(wkt_geom):
    """
    Takes a title geometry in well known text format and returns all address points that sit within that title geommetry - zero to many.
    """
    global url
    cql_filter_txt = 'WITHIN(shape,' + wkt_geom + ')'
    params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167', 'cql_filter': cql_filter_txt, 'outputFormat': 'application/json', 'propertyName': 'full_address'}
    url_plus_params = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(url_plus_params)
    addresses = []
    for address in data['full_address']:
         addresses.append(address)
    return addresses

# ---------------------------------

def get_titles_for_addresses(addresses):
    """
    Takes a list of addresses and returns them with their titles (zero to many per address)
    """
    address_title_dict = {}
    # first make wfs calls to get wkt geom for each address
    for address in addresses:
        address_title_dict[address] = {}
        address_title_dict[address]['wkt_geom'] = get_address_wkt_geom(address)

    # then make a second call to get the titles for each address point (wkt geom)
    for address in addresses:
        address_title_dict[address]['titles'] = get_titles_for_wkt_geom(address_title_dict[address]['wkt_geom'])
    return address_title_dict


def get_address_wkt_geom(address):
    """
    Takes a address string and returns the geometric point of that address wkt format
    """
    global url
    params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167', 'cql_filter': "full_address='" + address + "'", 'outputFormat': 'application/json'}
    url_plus_params = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(url_plus_params)
    # the data comes in lon lat order, which is not the format that WFS wants.  So we need to flip the order
    wkt_outline = re.sub(r'(\d+[.]\d+)\s+([-]\d+[.]\d+)', r'\2 \1',  str(data['geometry'][0])) 
    return wkt_outline


def get_titles_for_wkt_geom(wkt_geom):
    """
    Takes a address geometry in well known text format and returns all titles that encompass that address geommetry - zero to many.
    """
    global url
    cql_filter_txt = 'CONTAINS(shape,' + wkt_geom + ')'
    params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167', 'cql_filter': cql_filter_txt, 'outputFormat': 'application/json', 'propertyName': 'title_no'}
    url_plus_params = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(url_plus_params)
    titles = []
    for title in data['title_no']:
         titles.append(title)
    return titles


if __name__ == "__main__":
    addresses = get_addresses_for_titles(["95831","CB9A/258","CB655/91","325158","CB16K/805"])
    titles = get_titles_for_addresses(['2 Kajens Court, Lincoln'])
