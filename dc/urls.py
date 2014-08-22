# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from boski.views.base import TemplateTextPlainView

from module.web.views import IndexView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^robots\.txt$',
        TemplateTextPlainView.as_view(template_name='robots.txt')
    ),
    url(
        r'^$',
        IndexView.as_view(),
        name='index',
    ),
    (
        r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
    ),
    (
        r'^about/',
        include('module.about.urls', namespace='about')
    ),
    (
        r'^cms/',
        include('module.cms.urls', namespace='cms')
    ),
    (
        r'^blog/',
        include('module.blog.urls', namespace='blog')
    ),
    (
        r'^portfolio/',
        include('module.portfolio.urls', namespace='portfolio')
    ),
    (
        r'^',
        include('module.static_page.urls', namespace='static_page')
    ),
)
