""" Url router for the administration site
"""
from django.contrib import admin
from django.urls import re_path

from core_elasticsearch_app.views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    re_path(r'^templates', admin_views.TemplatesView.as_view(),
            name='core_elasticsearch_app_templates'),
    re_path(r'^template/add', admin_ajax.AddElasticsearchTemplateView.as_view(),
            name='core_elasticsearch_app_templates_add'),
    re_path(r'^template/(?P<pk>[\w-]+)/delete/$',
            admin_ajax.DeleteElasticsearchTemplateView.as_view(),
            name='core_elasticsearch_app_templates_delete'),
    re_path(r'^template/(?P<pk>[\w-]+)/edit/$',
            admin_ajax.EditElasticsearchTemplateView.as_view(),
            name='core_elasticsearch_app_templates_edit'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
