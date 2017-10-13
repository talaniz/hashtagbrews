from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.client import IndicesClient


class TestSearch(TestCase):

    def setUp(self):
        self.es = Elasticsearch()
        self.client = IndicesClient(client=self.es)

    def test_push_hop_to_index_creates_index(self):
        self.out = StringIO()
        call_command('push_hop_to_index', stdout=self.out)
        self.es_hop_index = self.client.get_mapping(index='hop')['hop']['mappings']['hop']['properties']

        self.id_type = self.es_hop_index['id']['type']
        self.name_type = self.es_hop_index['name']['type']
        self.min_alpha_acid_type = self.es_hop_index['min_alpha_acid']['type']
        self.max_alpha_acid_type = self.es_hop_index['max_alpha_acid']['type']
        self.country_type = self.es_hop_index['country']['type']
        self.comments_type = self.es_hop_index['comments']['type']

        self.assertEqual(self.id_type, 'long')

        self.assertEqual(self.name_type, 'text')
        self.assertEqual(self.min_alpha_acid_type, 'double')
        self.assertEqual(self.max_alpha_acid_type, 'double')

        self.assertEqual(self.country_type, 'text')
        self.assertEqual(self.comments_type, 'text')

    def test_push_grain_to_index_creates_index(self):
        self.out = StringIO()
        call_command('push_grain_to_index', stdout=self.out)
        self.es_grain_index = self.client.get_mapping(index='grain')['grain']['mappings']['grain']['properties']

        self.id_type = self.es_grain_index['id']['type']
        self.name_type = self.es_grain_index['name']['type']
        self.degrees_lovibond_type = self.es_grain_index['degrees_lovibond']['type']
        self.specific_gravity_type = self.es_grain_index['specific_gravity']['type']
        self.grain_type = self.es_grain_index['grain_type']['type']
        self.comments_type = self.es_grain_index['comments']['type']

        self.assertEqual(self.id_type, 'long')
        try:
            self.assertEqual(self.name_type, 'string')
        except AssertionError:
            self.assertEqual(self.name_type, 'text')
        self.assertEqual(self.degrees_lovibond_type, 'double')
        self.assertEqual(self.specific_gravity_type, 'double')
        try:
            self.assertEqual(self.grain_type, 'string')
        except AssertionError:
            self.assertEqual(self.grain_type, 'text')
        try:
            self.assertEqual(self.comments_type, 'string')
        except AssertionError:
            self.assertEqual(self.comments_type, 'text')
