#!/usr/bin/python3
from requests import Request
import geopandas as gpd
import re 

my_key = 'dfe042e3ee1445e1be1c7c4daa2f5b2b'
unaddressed_titles = ['95831','CB9A/258','CB655/91','325158','CB16K/805']

url = 'https://data.linz.govt.nz/services;key=' + my_key + '/wfs?service=WFS&version=2.0.0'

addressed_titles = {}
for title_no in unaddressed_titles:
    addressed_titles[title_no] = []
    params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167', 'cql_filter': "title_no='" + title_no + "'", 'outputFormat': 'application/json'}
    q = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(q)
    for geom in data['geometry']:
        # swap lat and lon into the required (in)correct order
        geom_str = re.sub(r'(\d+[.]\d+)\s+([-]\d+[.]\d+)', r'\2 \1', str(geom))
        cql_filter_txt = 'WITHIN(shape,' + geom_str + ')'
        params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167', 'cql_filter': cql_filter_txt, 'outputFormat': 'application/json', 'propertyName': 'full_address'}
        q = Request('POST', url, params=params).prepare().url
        data = gpd.read_file(q)
        for address in data['full_address']:
            addressed_titles[title_no].append(address)
1 + 1