""" Elasticsearch Ajax
"""
from django.urls import reverse_lazy

from core_elasticsearch_app.components.elasticsearch_template import api as elasticsearch_template_api
from core_elasticsearch_app.components.elasticsearch_template.models import ElasticsearchTemplate
from core_elasticsearch_app.views.admin.forms import ElasticsearchTemplateForm
from core_main_app.views.common.ajax import AddObjectModalView, DeleteObjectModalView, EditObjectModalView


class AddElasticsearchTemplateView(AddObjectModalView):
    """ AddElasticsearchTemplateView
    """
    form_class = ElasticsearchTemplateForm
    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = 'Template was successfully configured for Elasticsearch.'

    def _save(self, form):
        # Save treatment.
        try:
            es_template = ElasticsearchTemplate(template=self.object.template,
                                                title_path=self.object.title_path,
                                                description_path=self.object.description_path)
            elasticsearch_template_api.upsert(es_template)
        except Exception as e:
            form.add_error(None, str(e))


class EditElasticsearchTemplateView(EditObjectModalView):
    """ EditElasticsearchTemplateView
    """
    form_class = ElasticsearchTemplateForm
    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = 'Template Configuration edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            elasticsearch_template_api.upsert(self.object)
        except Exception as e:
            form.add_error(None, str(e))


class DeleteElasticsearchTemplateView(DeleteObjectModalView):
    """ DeleteElasticsearchTemplateView
    """
    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = 'Template Configuration deleted with success.'

    def _delete(self, request, *args, **kwargs):
        # Delete treatment.
        elasticsearch_template_api.delete(self.object)

    def _get_object_name(self):
        return "the configuration using the template {0}"\
            .format(self.object.template.display_name)
