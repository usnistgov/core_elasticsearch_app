""" Settings for core_elasticsearch_app.
These settings are overwritten at project level.
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

ELASTICSEARCH_HOST = getattr(settings, 'ELASTICSEARCH_HOST', 'localhost')
""" :py:class:`str`: Elasticsearch host
"""

ELASTICSEARCH_PORT = getattr(settings, 'ELASTICSEARCH_PORT', 9200)
""" :py:class:`int`: Elasticsearch port
"""

CAN_SET_PUBLIC_DATA_TO_PRIVATE = getattr(settings, 'CAN_SET_PUBLIC_DATA_TO_PRIVATE', False)
""" :py:class:`boolean`: True if public data can be unpublished
"""

ELASTICSEARCH_DATA_TITLE = getattr(settings, "ELASTICSEARCH_DATA_TITLE", lambda data: data.title)
""" Select a path in the data to be indexed as the data's title
"""
# ELASTICSEARCH_DATA_TITLE = lambda data: data.dict_content['Resource']['identity']['title']

ELASTICSEARCH_DATA_DESCRIPTION = getattr(settings, "ELASTICSEARCH_DATA_DESCRIPTION", lambda data: None)
""" Select a path in the data to indexed as the data's description
"""
# ELASTICSEARCH_DATA_DESCRIPTION = lambda data: data.dict_content['Resource']['content']['description']
# TODO: see how we can index all the text content of a data

