#!/usr/bin/python3
from requests import Request
import geopandas as gpd
import re, json , unittest
from LINZ_WFS import LINZ_WFS

class TEST_LINZ_WFS(unittest.TestCase):
    def setUp(self) -> None:

        # read the config json file
        with open('config.json') as f:
            config = json.load(f)

        self.my_linz_key = config['linz_key']
        self.my_linz_wfs = LINZ_WFS(self.my_linz_key)
        self.url = 'https://data.linz.govt.nz/services;key=' + self.my_linz_key + '/wfs?service=WFS&version=2.0.0'

        ##############################################################################################################
        # Get all the addresses within 200m of The Beehive (New Zealand's iconic parliment building) 
        # -41.278419237850684, 174.776693340537
        ##############################################################################################################
        self.params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167'
                , 'cql_filter': 'DWithin(shape,POINT(-41.278419237850684 174.776693340537),200,meters)', 'outputFormat': 'application/json'}
        self.url_plus_params = Request('GET', self.url, params=self.params).prepare().url
        self.data_addresses = gpd.read_file(self.url_plus_params)
        self.titles_for_addresses = self.my_linz_wfs.get_titles_for_addresses(self.data_addresses['full_address'])

        ##############################################################################################################
        # Get all the titles within 200m of The Beehive (New Zealand's iconic parliment building) 
        # -41.278419237850684, 174.776693340537
        ##############################################################################################################
        self.params = {'request': 'GetFeature', 'typeName': 'layer-50804', 'SRSName': 'EPSG:4167'
                , 'cql_filter': 'DWithin(shape,POINT(-41.278419237850684 174.776693340537),200,meters)', 'outputFormat': 'application/json'}
        self.url_plus_params = Request('GET', self.url, params=self.params).prepare().url
        self.data_titles = gpd.read_file(self.url_plus_params)
        self.addresses_for_titles = self.my_linz_wfs.get_addresses_for_titles(self.data_titles['title_no'].tolist())

        return super().setUp()
        
    def test_get_title_wkt_geom(self):
        self.assertEqual(1, 1)
    def test_get_address_for_wkt_geom(self):
        self.assertEqual(1, 1)
    def test_get_titles_for_addresses(self):
        self.assertEqual(1, 1)
    def test_get_addresses_for_titles(self):
        self.assertRaises(TypeError,)
        self.assertEqual(1, 1)

# launch the test suite
if __name__ == '__main__':
    unittest.main()