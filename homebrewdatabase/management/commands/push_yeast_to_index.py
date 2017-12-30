from elasticsearch.client import IndicesClient
from elasticsearch import Elasticsearch, RequestsHttpConnection

from django.core.management.base import BaseCommand

ES_CLIENT = Elasticsearch(
    ['http://127.0.0.1:9200/'],
    connection_class=RequestsHttpConnection
)

es_mapping = {
    'properties': {
        'id': {
            'type': 'long'
                    },
        'name': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
                    },
        'user': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'lab': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'yeast_type': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'yeast_form': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'min_temp': {
            'type': 'integer'
        },
        'max_temp': {
            'type': 'integer'
        },
        'attenuation': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'flocculation': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        'comments': {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
    }
}


class Command(BaseCommand):

    help = "Command to create yeast index in elasticsearch"

    def handle(self, *args, **kwargs):
        self.recreate_index()

    def recreate_index(self):
        indices_client = IndicesClient(client=ES_CLIENT)

        index_name = 'yeast'
        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)
        indices_client.create(index=index_name)
        indices_client.put_mapping(
            doc_type='yeast',
            body=es_mapping,
            index=index_name
        )
