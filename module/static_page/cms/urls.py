#-*- coding:utf-8 -*-
from django.conf.urls import *

from module.static_page.cms.views import List

urlpatterns = patterns('module.static_page.cms.views',
    url(r'^$', List.as_view(), name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^activate/(?P<pk>[\d]+)/$', 'activate', name='activate'),
    url(r'^update/(?P<pk>[\d]+)/$', 'update', name='update'),
    url(r'^delete/(?P<pk>[\d]+)/$', 'delete', name='delete'),
)
