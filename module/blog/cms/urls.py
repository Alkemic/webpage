# -*- coding:utf-8 -*-
from django.conf.urls import *

from .views import List, Update, Create, Delete


__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

urlpatterns = patterns(
    'module.blog.cms.views',
    url(r'create/$', Create.as_view(), name='create'),
    url(r'toggle_active/(?P<pk>[\d]+)/$', 'toggle_active', name='toggle-active'),
    url(r'update/(?P<pk>[\d]+)/$', Update.as_view(), name='update'),
    url(r'delete/(?P<pk>[\d]+)/$', Delete.as_view(), name='delete'),
    url(r'/?$', List.as_view(), name='index'),
)
