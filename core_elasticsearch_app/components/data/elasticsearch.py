""" Utils for managing CDCS data in elasticsearch
"""
import logging

from core_elasticsearch_app.commons.exceptions import ElasticsearchError
from core_elasticsearch_app.components.data.autocomplete_settings import DATA_AUTOCOMPLETE_SETTINGS
from core_elasticsearch_app.components.elasticsearch_template import api as elasticsearch_template_api
from core_elasticsearch_app.settings import ELASTICSEARCH_CDCS_DATA_INDEX
from core_elasticsearch_app.utils.elasticsearch_client import ElasticsearchClient
from core_elasticsearch_app.utils.utils import get_nested_value

logger = logging.getLogger(__name__)


def create_title_autocomplete_index():
    """ Create autocomplete index on data titles

    Returns:

    """
    return ElasticsearchClient.create_index(ELASTICSEARCH_CDCS_DATA_INDEX, DATA_AUTOCOMPLETE_SETTINGS)


def index_data(data):
    """ Build json document for elasticsearch from CDCS data

    Args:
        data:

    Returns:

    """
    es_template = elasticsearch_template_api.get_by_template(data.template)
    if es_template:
        es_data = {
            'data_id': str(data.id),
            'title': get_value_from_path(data, es_template.title_path),
            'description': get_value_from_path(data, es_template.description_path)
        }
        # TODO: could use global PID instead of id
        return ElasticsearchClient.index_document(ELASTICSEARCH_CDCS_DATA_INDEX, str(data.id), es_data)


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
    result = ElasticsearchClient.search(ELASTICSEARCH_CDCS_DATA_INDEX, query)
    return result['hits']['hits']


def get_value_from_path(data, path):
    """

    Args:
        data:
        path:

    Returns:

    """
    value = get_nested_value(data.dict_content, path)
    if value:
        if isinstance(value, dict):
            logger.info("A dict was found at {0} for data {1}".format(path, str(data.id)))
            try:
                value = value["#text"]
            except:
                value = None
                logger.warning("#text was not found at path {0} for data {1}".format(path, str(data.id)))
    else:
        logger.warning("No value could be found at path {0} for data {1}".format(path, str(data.id)))
    return value
