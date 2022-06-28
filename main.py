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
    Takes a list of titles and return them with their addresses (zero to many per title)
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
    Takes a title and returns a list of coordinates in wkt format, with lon lat swapped to lat lon 
    """
    global url
    params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167', 'cql_filter': "title_no='" + title_no + "'", 'outputFormat': 'application/json'}
    url_plus_params = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(url_plus_params)
    1 + 1
    wkt_outline = re.sub(r'(\d+[.]\d+)\s+([-]\d+[.]\d+)', r'\2 \1',  str(data['geometry'][0])) # swap lon lat to lat lon 
    return wkt_outline


def get_address_for_wkt_geom(wkt_geom):
    """
    Takes a wkt_geom and returns an address
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


if __name__ == "__main__":
    get_addresses_for_titles(["95831","CB9A/258","CB655/91","325158","CB16K/805"])


#addressed_titles = {}
#for title_no in config['unaddressed_titles']:
#    addressed_titles[title_no] = []
#    params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167', 'cql_filter': "title_no='" + title_no + "'", 'outputFormat': 'application/json'}
#    q = Request('GET', url, params=params).prepare().url
#    data = gpd.read_file(q)
#    for geom in data['geometry']:
#        # swap lat and lon into the required (in)correct order
#        geom_str = re.sub(r'(\d+[.]\d+)\s+([-]\d+[.]\d+)', r'\2 \1', str(geom))
#        cql_filter_txt = 'WITHIN(shape,' + geom_str + ')'
#        params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167', 'cql_filter': cql_filter_txt, 'outputFormat': 'application/json', 'propertyName': 'full_address'}
#        q = Request('POST', url, params=params).prepare().url
#        data = gpd.read_file(q)
#        for address in data['full_address']:
#            addressed_titles[title_no].append(address)
#
## output the results to the file in config['output_file']
#with open(config['output_file'], 'w') as f:
#    # set the output format to match the extension of config['output_file']
#    if config['output_file'].endswith('.json'):
#        json.dump(addressed_titles, f, indent=4)
#    elif config['output_file'].endswith('.csv'):
#        for title_no in addressed_titles:
#            f.write(title_no + ',' + ','.join(addressed_titles[title_no]) + '\n')
#    else:
#        print('Unknown output file extension')
#        exit(1)
