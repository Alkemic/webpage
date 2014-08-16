# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from boski.views.base import TemplateTextPlainView


admin.autodiscover()

if getattr(settings, 'IS_WIP', False):
    index_entry = url(
        r'^$',
        TemplateTextPlainView.as_view(template_name='wip.txt'),
        name='index',
    )
else:
    index_entry = url(
        r'^$',
        RedirectView.as_view(pattern_name='blog:index'),
        name='index',
    )

urlpatterns = patterns(
    '',
    url(
        r'^robots\.txt$',
        TemplateTextPlainView.as_view(template_name='robots.txt')
    ),
    index_entry,
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
