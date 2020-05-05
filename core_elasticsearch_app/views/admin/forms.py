""" Elasticsearch forms
"""
from django import forms
from django_mongoengine.forms import DocumentForm

from core_elasticsearch_app.components.elasticsearch_template.models import ElasticsearchTemplate
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api


class ElasticsearchTemplateForm(DocumentForm):
    """ ElasticsearchTemplate form
    """
    template = forms.ChoiceField(label='Template',
                                 widget=forms.Select(attrs={"class": "form-control"}))

    title_path = forms.CharField(label='Path to Title', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Resource/identity/title',
                                                               'class': 'form-control'}))

    description_path = forms.CharField(label='Path to Description', required=False,
                                       widget=forms.TextInput(attrs={'placeholder': 'Resource/content/description',
                                                                     'class': 'form-control'}))

    class Meta(object):
        document = ElasticsearchTemplate
        fields = ['template', 'title_path', 'description_path']

    def __init__(self, *args, **kwargs):
        super(ElasticsearchTemplateForm, self).__init__(*args, **kwargs)
        self.fields['template'].choices = _get_templates_versions()

    def clean_template(self):
        data = self.cleaned_data['template']
        return template_api.get(data)


# FIXME: duplicate from core_oaipmh_provider_app
def _get_templates_versions():
    """ Get templates versions.

    Returns:
        List of templates versions.

    """
    templates = []
    try:
        list_ = template_version_manager_api.get_active_global_version_manager()
        for elt in list_:
            for version in elt.versions:
                template = template_api.get(version)
                version_name = template.display_name
                templates.append((version, version_name))
    except exceptions.DoesNotExist as e:
        logger.warning("_get_templates_versions threw an exception: {0}".format(str(e)))

    return templates
