#!/usr/bin/python3
from requests import Request
import geopandas as gpd


url = 'https://data.linz.govt.nz/services;key=dfe042e3ee1445e1be1c7c4daa2f5b2b/wfs?service=WFS&version=2.0.0'
params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:2193', 'cql_filter': 'title_no=95831', 'outputFormat': 'application/json'}
q = Request('GET', url, params=params).prepare().url
data = gpd.read_file(q)

cql_filter_txt = 'Within(shape,' + data.iloc[0]['geometry'] + ')'
params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:2193', 'cql_filter': cql_filter_txt``, 'outputFormat': 'application/json'}
q = Request('GET', url, params=params).prepare().url
data = gpd.read_file(q)
1 + 1