from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.six import StringIO

from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.client import IndicesClient


class TestSearch(TestCase):

    def setUp(self):
        self.es = Elasticsearch()
        self.client = IndicesClient(client=self.es)
        self.user = User.objects.create_user(username='testuser', email="antonio.alaniz@gmail.com",
                                             password='testpassword')

    def test_push_hop_to_index_creates_index(self):
        self.out = StringIO()
        call_command('push_hop_to_index', stdout=self.out)
        self.es_hop_index = self.client.get_mapping(index='hop')['hop']['mappings']['hop']['properties']

        self.id_type = self.es_hop_index['id']['type']
        self.user_type = self.es_hop_index['user']['type']
        self.name_type = self.es_hop_index['name']['type']
        self.min_alpha_acid_type = self.es_hop_index['min_alpha_acid']['type']
        self.max_alpha_acid_type = self.es_hop_index['max_alpha_acid']['type']
        self.country_type = self.es_hop_index['country']['type']
        self.comments_type = self.es_hop_index['comments']['type']

        self.assertEqual(self.id_type, 'long')

        self.assertEqual(self.name_type, 'text')
        self.assertEqual(self.user_type, 'text')
        self.assertEqual(self.min_alpha_acid_type, 'double')
        self.assertEqual(self.max_alpha_acid_type, 'double')

        self.assertEqual(self.country_type, 'text')
        self.assertEqual(self.comments_type, 'text')

    def test_push_grain_to_index_creates_index(self):
        self.out = StringIO()
        call_command('push_grain_to_index', stdout=self.out)
        self.es_grain_index = self.client.get_mapping(index='grain')['grain']['mappings']['grain']['properties']

        self.id_type = self.es_grain_index['id']['type']
        self.user_type = self.es_grain_index['user']['type']
        self.name_type = self.es_grain_index['name']['type']
        self.degrees_lovibond_type = self.es_grain_index['degrees_lovibond']['type']
        self.specific_gravity_type = self.es_grain_index['specific_gravity']['type']
        self.grain_type = self.es_grain_index['grain_type']['type']
        self.comments_type = self.es_grain_index['comments']['type']

        self.assertEqual(self.id_type, 'long')
        self.assertEqual(self.user_type, 'text')
        self.assertEqual(self.name_type, 'text')
        self.assertEqual(self.degrees_lovibond_type, 'double')
        self.assertEqual(self.specific_gravity_type, 'double')
        self.assertEqual(self.grain_type, 'text')
        self.assertEqual(self.comments_type, 'text')

    def test_push_yeast_to_index_creates_index(self):
        self.out = StringIO()
        call_command('push_yeast_to_index', stdout=self.out)
        self.es_yeast_index = self.client.get_mapping(index='yeast')['yeast']['mappings']['yeast']['properties']

        self.id_type = self.es_yeast_index['id']['type']
        self.user_type = self.es_yeast_index['user']['type']
        self.name_type = self.es_yeast_index['name']['type']
        self.lab_type = self.es_yeast_index['lab']['type']
        self.yeast_type_type = self.es_yeast_index['yeast_type']['type']
        self.yeast_form_type = self.es_yeast_index['yeast_form']['type']
        self.min_temp_type = self.es_yeast_index['min_temp']['type']
        self.max_temp_type = self.es_yeast_index['max_temp']['type']
        self.attenuation_type = self.es_yeast_index['attenuation']['type']
        self.flocculation_type = self.es_yeast_index['flocculation']['type']
        self.comments_type = self.es_yeast_index['comments']['type']

        self.assertEqual(self.id_type, 'long')
        self.assertEqual(self.user_type, 'text')
        self.assertEqual(self.name_type, 'text')
        self.assertEqual(self.lab_type, 'text')
        self.assertEqual(self.yeast_type_type, 'text')
        self.assertEqual(self.yeast_form_type, 'text')
        self.assertEqual(self.min_temp_type, 'integer')
        self.assertEqual(self.max_temp_type, 'integer')
        self.assertEqual(self.attenuation_type, 'text')
        self.assertEqual(self.flocculation_type, 'text')
        self.assertEqual(self.comments_type, 'text')
