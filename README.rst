======================
Core Elasticsearch App
======================

Elasticsearch utils for the curator core project.

Quick start
===========

1. Add "core_elasticsearch_app" to your INSTALLED_APPS setting
--------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_elasticsearch_app',
    ]

The package should be placed above `core_explore_keyword_app` in the `INSTALLED_APPS` to enable autocomplete powered
by elasticsearch.

2. Include the core_elasticsearch_app URLconf in your project urls.py
---------------------------------------------------------------------

.. code:: python

    url(r'^elasticsearch/', include('core_elasticsearch_app.urls')),
