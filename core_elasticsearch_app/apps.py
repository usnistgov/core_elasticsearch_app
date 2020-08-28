""" Apps file for setting elasticsearch when app is ready
"""
import sys

from django.apps import AppConfig

from core_elasticsearch_app.commons.exceptions import ElasticsearchError
from core_elasticsearch_app.components.data import watch as data_watch
from core_elasticsearch_app.components.data.elasticsearch import (
    create_title_autocomplete_index,
)
from core_elasticsearch_app.settings import CAN_SET_PUBLIC_DATA_TO_PRIVATE


class ElasticsearchAppConfig(AppConfig):
    """Core application settings"""

    name = "core_elasticsearch_app"

    def ready(self):
        """Run when the app is ready

        Returns:

        """
        if "migrate" not in sys.argv:
            if CAN_SET_PUBLIC_DATA_TO_PRIVATE:
                raise ElasticsearchError(
                    "The Elasticsearch app will only work for systems where "
                    "CAN_SET_PUBLIC_DATA_TO_PRIVATE is set to False."
                )
            create_title_autocomplete_index()
            data_watch.init()
