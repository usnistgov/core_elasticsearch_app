""" Utils for managing CDCS data in elasticsearch
"""
from core_elasticsearch_app.components.data.autocomplete_settings import DATA_AUTOCOMPLETE_SETTINGS
from core_elasticsearch_app.settings import ELASTICSEARCH_DATA_TITLE, ELASTICSEARCH_DATA_DESCRIPTION
from core_elasticsearch_app.utils.elasticsearch_client import ElasticsearchClient

INDEX_NAME = 'cdcs-data'


def create_title_autocomplete_index():
    """ Create autocomplete index on data titles

    Returns:

    """
    return ElasticsearchClient.create_index(INDEX_NAME, DATA_AUTOCOMPLETE_SETTINGS)


def index_data(data):
    """ Build json document for elasticsearch from CDCS data

    Args:
        data:

    Returns:

    """
    es_data = {
        'data_id': str(data.id),
        'title': ELASTICSEARCH_DATA_TITLE(data),
        'description': ELASTICSEARCH_DATA_DESCRIPTION(data)
    }
    # TODO: could use global PID instead of id
    return ElasticsearchClient.index_document(INDEX_NAME, str(data.id), es_data)


def get_suggestions(query, fuzziness=1, prefix_length=3, fragment_size=100):
    """ Get suggestions from query

    Args:
        query:
        fuzziness:
        prefix_length:
        fragment_size:

    Returns:

    """
    query = {
        "query": {
            "multi_match": {
                "query": query,
                "fuzziness": fuzziness,
                "prefix_length": prefix_length
            }
        },
        "highlight": {
            "number_of_fragments": 1,
            "fragment_size": fragment_size,
            "fields": {
                "title": {},
                "description": {}
            }
        }
    }
    result = ElasticsearchClient.search(INDEX_NAME, query)
    return result['hits']['hits']
