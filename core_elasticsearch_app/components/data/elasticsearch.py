""" Utils for managing CDCS data in elasticsearch
"""
import logging

from core_elasticsearch_app.components.data.autocomplete_settings import (
    DATA_AUTOCOMPLETE_SETTINGS,
)
from core_elasticsearch_app.components.data.semantic_search_settings import (
    DATA_SEMANTIC_SEARCH_SETTINGS,
)
from core_elasticsearch_app.components.data.mongodb import get_value_from_path
from core_elasticsearch_app.components.elasticsearch_template import (
    api as elasticsearch_template_api,
)
from core_elasticsearch_app.settings import ELASTICSEARCH_CDCS_DATA_INDEX, ELASTICSEARCH_CDCS_DATA_INDEX_SEMANTIC
from core_elasticsearch_app.utils.elasticsearch_client import ElasticsearchClient
from core_main_app.commons import exceptions
from bert_serving.client import BertClient

logger = logging.getLogger(__name__)


def create_title_autocomplete_index():
    """Create autocomplete index on data titles

    Returns:

    """
    return ElasticsearchClient.create_index(
        ELASTICSEARCH_CDCS_DATA_INDEX, DATA_AUTOCOMPLETE_SETTINGS
    )


def create_title_semantic_search_index():
    """Create autocomplete index on data titles

    Returns:

    """
    return ElasticsearchClient.create_index(
        ELASTICSEARCH_CDCS_DATA_INDEX_SEMANTIC, DATA_SEMANTIC_SEARCH_SETTINGS
    )


def index_data(data):
    """Build json document for elasticsearch from CDCS data

    Args:
        data:

    Returns:

    """
    try:
        es_template = elasticsearch_template_api.get_by_template(data.template)
        es_data = {
            "data_id": str(data.id),
            "title": get_value_from_path(data, es_template.title_path),
            "description": " ".join(
                [
                    _get_string_value(get_value_from_path(data, path))
                    for path in es_template.description_paths
                ]
            ),
        }
        # TODO: could use global PID instead of id
        return ElasticsearchClient.index_document(
            ELASTICSEARCH_CDCS_DATA_INDEX, str(data.id), es_data
        )
    except exceptions.DoesNotExist:
        logger.warning(
            "Data with id {0} will not be indexed. No template configured.".format(
                str(data.id)
            )
        )
    except Exception as e:
        logger.error(str(e))


def index_data_semantic(data):
    """Build json document for elasticsearch from CDCS data

    Args:
        data:

    Returns:

    """
    try:
        bc = BertClient(output_fmt='list')

        es_template = elasticsearch_template_api.get_by_template(data.template)
        description = " ".join(
            [
                _get_string_value(get_value_from_path(data, path))
                for path in es_template.description_paths
            ])

        emb = bc.encode([description]) # passing an array because encode() can process multiple entities
        es_data = {
            "data_id": str(data.id),
            "title": get_value_from_path(data, es_template.title_path),
            "description": description,
            "text_vector": emb[0] # retrieves only the first embedding because we encoded only one element
        }

        return ElasticsearchClient.index_document(
            ELASTICSEARCH_CDCS_DATA_INDEX_SEMANTIC, str(data.id), es_data
        )
    except exceptions.DoesNotExist:
        logger.warning(
            "Data with id {0} will not be indexed. No template configured.".format(
                str(data.id)
            )
        )
    except Exception as e:
        logger.error(str(e))


def get_suggestions(query, fuzziness=1, prefix_length=3, fragment_size=100):
    """Get suggestions from query

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
                "prefix_length": prefix_length,
            }
        },
        "highlight": {
            "number_of_fragments": 1,
            "fragment_size": fragment_size,
            "fields": {"title": {}, "description": {}},
        },
    }
    result = ElasticsearchClient.search(ELASTICSEARCH_CDCS_DATA_INDEX, query)
    return result["hits"]["hits"]


def get_semantic_suggestions(query):
    """Get semantic suggestions from query

    Args:
        query:

    Returns:
        suggestions

    """

    bc = BertClient(output_fmt='list')

    query_vector = bc.encode([query])[0]

    query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    result = ElasticsearchClient.search(
        ELASTICSEARCH_CDCS_DATA_INDEX_SEMANTIC,
        {
            "query": query,
            "_source": {"includes": ["title", "text"]}
        })

    return result["hits"]["hits"]


def _get_string_value(value):
    """Get string value

    Args:
        value:

    Returns:

    """
    if value:
        return value
    return ""
