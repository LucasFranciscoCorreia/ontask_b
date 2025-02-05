# -*- coding: utf-8 -*-

"""First entry point to define URLs."""

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import path
from django.utils.translation import ugettext
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog
from rest_framework.documentation import include_docs_urls

import ontask.accounts.urls
import ontask.action.urls
import ontask.dataops.urls
import ontask.logs.urls
import ontask.oauth.urls
import ontask.profiles.urls
import ontask.scheduler.urls
import ontask.table.urls
import ontask.workflow.urls
import ontask.workflow.views.home
from ontask.core import views
from ontask.dataops.pandas import set_engine
from ontask.templatetags.ontask_tags import ontask_version
from ontask.workflow.views import home

api_description = ugettext(
    'The OnTask API offers functionality to manipulate workflows, tables '
    + 'and logs. The interface provides CRUD operations over these '
    + 'objects.')

urlpatterns = [
    # Home Page!
    path('', home, name='home'),

    path('lti_entry', views.lti_entry, name='lti_entry'),

    path('not_authorized', ontask.workflow.views.home, name='not_authorized'),

    path('about', views.AboutPage.as_view(), name='about'),

    path(
        'under_construction',
        views.under_construction,
        name='under_construction'),

    path('users', include(ontask.profiles.urls, namespace='profiles')),

    path('ota', admin.site.urls),

    path('trck', views.trck, name='trck'),

    path('keep_alive', views.keep_alive, name='keep_alive'),

    path('', include(ontask.accounts.urls, namespace='accounts')),

    path('workflow/', include(ontask.workflow.urls, namespace='workflow')),

    path('dataops/', include(ontask.dataops.urls, namespace='dataops')),

    path('action/', include(ontask.action.urls, namespace='action')),

    path('table/', include(ontask.table.urls, namespace='table')),

    path('scheduler/', include(ontask.scheduler.urls, namespace='scheduler')),

    path('logs/', include(ontask.logs.urls, namespace='logs')),

    path('summernote/', include('django_summernote.urls')),

    path(
        'ontask_oauth/',
        include(ontask.oauth.urls,
                namespace='ontask_oauth')),

    path('tobedone', views.ToBeDone.as_view(), name='tobedone'),

    # API AUTH and DOC
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),

    path(
        'apidoc/',
        include_docs_urls(
            title='OnTask API',
            description=api_description,
            public=False),
    ),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path(
        'jsi18n',
        cache_page(
            86400,
            key_prefix='js18n-%s' % ontask_version())(
            JavaScriptCatalog.as_view()),
        name='javascript-catalog',
    ),
)

# Include django debug toolbar if DEBUG is ons
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]

handler400 = 'ontask.core.views.ontask_handler400'
handler403 = 'ontask.core.views.ontask_handler403'
handler404 = 'ontask.core.views.ontask_handler404'
handler500 = 'ontask.core.views.ontask_handler500'

# Create the DB engine with SQLAlchemy (once!)
set_engine()

# Make sure the Site has the right information
try:
    site = Site.objects.get(id=settings.SITE_ID)
    site.domain = settings.DOMAIN_NAME
    site.name = settings.DOMAIN_NAME
    site.save()
except Exception:
    # To bypass the migrate command execution that fails because the Site
    # table is not created yet.
    site = None

# Remove from AVAILABLE_ACTION_TYPES those in DISABLED_ACTIONS
try:
    eval_obj = [eval(daction) for daction in settings.DISABLED_ACTIONS]
    for atype in eval_obj:
        to_remove = next(
            afull_type for afull_type in ontask.ACTION_TYPES
            if afull_type[0] == atype)
        ontask.AVAILABLE_ACTION_TYPES.remove(to_remove)
except Exception:
    raise Exception(
        'Unable to configure available action types. '
        + 'Review variable DISABLED_ACTIONS')
