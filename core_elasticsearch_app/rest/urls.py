""" Url router for the core elasticsearch app
"""
from django.conf.urls import url

from core_elasticsearch_app.rest.views import DocumentSuggestion, KeywordSuggestion

urlpatterns = [
    url(
        r"^document/suggest",
        DocumentSuggestion.as_view(),
        name="core_elasticsearch_document_suggestion_view",
    ),
    url(
        r"^keyword/suggest",
        KeywordSuggestion.as_view(),
        name="core_elasticsearch_keyword_suggestion_view",
    ),
]
