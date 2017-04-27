from elasticsearch.client import IndicesClient
from elasticsearch import Elasticsearch, RequestsHttpConnection

from django.core.management.base import BaseCommand

ES_CLIENT = Elasticsearch(
    ['http://192.168.99.100:9200/'],
    connection_class=RequestsHttpConnection,
    http_auth=('elastic', 'changeme')
)

es_mapping = {
    'properties': {
        'id': {
            'type': 'long'
        },
        'name': {
            'type': 'string'
        },
        'degrees_lovibond': {
            'type': 'double'
        },
        'specific_gravity': {
            'type': 'double'
        },
        'grain_type': {
            'type': 'string'
        },
        'comments': {
            'type': 'string'
        }
    }
}


class Command(BaseCommand):

    help = "Command to create grain index in elasticsearc"

    def handle(self, *args, **kwargs):
        self.recreate_index()

    def recreate_index(self):
        indices_client = IndicesClient(client=ES_CLIENT)

        index_name = 'grain'
        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)
        indices_client.create(index=index_name)
        indices_client.put_mapping(
            doc_type='grain',
            body=es_mapping,
            index=index_name
        )