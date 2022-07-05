#!/usr/bin/python3
from requests import Request
import geopandas as gpd
import re, json , unittest

class TEST_LINZ_WFS(unittest.TestCase):
    def setUp(self) -> None:

        # read in my_linz_key from config.json
        with open('config.json') as f:
            self.config = json.load(f)
            self.my_linz_key = self.config['my_linz_key']

        self.url = 'https://data.linz.govt.nz/services;key=' + self.my_linz_key + '/wfs?service=WFS&version=2.0.0'

        # get all the addresses within 300m of the beehive -41.278419237850684, 174.776693340537
        self.params = {'request': 'GetFeature', 'typeName': 'layer-53353', 'SRSName': 'EPSG:4167'
                , 'cql_filter': 'DWithin(shape,POINT(-41.278419237850684 174.776693340537),300,meters)', 'outputFormat': 'application/json'}
        self.url_plus_params = Request('GET', self.url, params=self.params).prepare().url
        self.data = gpd.read_file(self.url_plus_params)

        self.my_linz_wfs = LINZ_WFS(config['access_key'])

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
    with open('config.json') as f:
        config = json.load(f)
    unittest.main()