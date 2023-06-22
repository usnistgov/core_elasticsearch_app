""" Url router for the core elasticsearch app
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r"rest/", include("core_elasticsearch_app.rest.urls")),
]
