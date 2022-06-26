#!/usr/bin/python3
from requests import Request
import geopandas as gpd
import re, json 

# load config dictionary from json file
with open('config.json') as f:
    config = json.load(f)


url = 'https://data.linz.govt.nz/services;key=' + config['my_linz_key'] + '/wfs?service=WFS&version=2.0.0'

addressed_titles = {}
for title_no in config['unaddressed_titles']:
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

# output the results to the file in config['output_file']
with open(config['output_file'], 'w') as f:
    # set the output format to match the extension of config['output_file']
    if config['output_file'].endswith('.json'):
        json.dump(addressed_titles, f, indent=4)
    elif config['output_file'].endswith('.csv'):
        for title_no in addressed_titles:
            f.write(title_no + ',' + ','.join(addressed_titles[title_no]) + '\n')
    else:
        print('Unknown output file extension')
        exit(1)
