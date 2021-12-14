""" ElasticsearchTemplate model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.validation.xpath_validation import validate_xpath_list


class ElasticsearchTemplate(models.Model):
    """ElasticsearchTemplate object"""

    template = models.OneToOneField(
        Template, blank=False, on_delete=models.CASCADE, unique=True
    )
    title_path = models.CharField(default=None, max_length=400)
    description_paths = models.JSONField(
        blank=False, validators=[validate_xpath_list], default=list
    )

    @staticmethod
    def get_by_id(es_template_id):
        """Returns the object with a given id

        Args:
            es_template_id:

        Returns:
            ElasticsearchTemplate (obj): ElasticsearchTemplate

        """
        try:
            return ElasticsearchTemplate.objects.get(pk=es_template_id)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_template(template):
        """Returns the object with a given template

        Args:
            template:

        Returns:
            ElasticsearchTemplate (obj): ElasticsearchTemplate

        """
        try:
            return ElasticsearchTemplate.objects.get(template=template)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all():
        """Returns all objects"""
        return ElasticsearchTemplate.objects.all()

    def __str__(self):
        """Elasticsearch template object as string

        Returns:

        """
        return self.template.__str__()
