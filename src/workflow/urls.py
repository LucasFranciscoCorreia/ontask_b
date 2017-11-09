# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import attribute_views, column_views, import_export_views
from . import views, api

app_name = 'workflow'

urlpatterns = [
    url(r'^$', views.workflow_index, name='index'),

    url(r'^create/$', views.WorkflowCreateView.as_view(), name='create'),

    url(r'^(?P<pk>\d+)/update/$', views.update, name='update'),

    url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),

    url(r'^(?P<pk>\d+)/flush/$', views.flush, name='flush'),

    url(r'^(?P<pk>\d+)/detail/$', views.WorkflowDetailView.as_view(),
        name='detail'),

    # Import Export

    url(r'^export_ask/$', import_export_views.export_ask, name='export_ask'),

    url(r'^export/$', import_export_views.export, name='export'),

    url(r'^import/$', import_export_views.import_workflow, name='import'),

    # Attributes

    url(r'^attributes/$', attribute_views.attributes, name='attributes'),

    url(r'^attribute_create/$',
        attribute_views.attribute_create,
        name='attribute_create'),

    url(r'^attribute_delete/$',
        attribute_views.attribute_delete,
        name='attribute_delete'),

    # Column manipulation

    url(r'^column_add/$', column_views.column_add, name='column_add'),

    url(r'^(?P<pk>\d+)/column_delete/$',
        column_views.column_delete,
        name='column_delete'),

    url(r'^(?P<pk>\d+)/column_edit/$',
        column_views.column_edit,
        name='column_edit'),

    # API

    url(r'^workflows/$', api.WorkflowAPIListCreate.as_view(),
        name='api_workflows'),

    url(r'^(?P<pk>\d+)/rud/$',
        api.WorkflowAPIRetrieveUpdateDestroy.as_view(), name='api_rud'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
