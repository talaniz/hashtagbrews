from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


class TestSearch(TestCase):

    def setUp(self):
        self.es = Elasticsearch()
        self.client = IndicesClient(client=self.es)

    def test_push_to_index_creates_index(self):
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
        self.assertEqual(self.name_type, 'string')
        self.assertEqual(self.min_alpha_acid_type, 'double')
        self.assertEqual(self.max_alpha_acid_type, 'double')
        self.assertEqual(self.country_type, 'string')
        self.assertEqual(self.comments_type, 'string')
