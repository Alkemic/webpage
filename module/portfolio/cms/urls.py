# -*- coding:utf-8 -*-
from django.conf.urls import *
from .views import List, Update, Create, Delete, CompanyList, CompanyCreate, CompanyUpdate, CompanyDelete

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

urlpatterns = patterns(
    'module.portfolio.cms.views',
    url(r'company/create/$', CompanyCreate.as_view(), name='company-create'),
    url(r'company/update/(?P<pk>[\d]+)/$', CompanyUpdate.as_view(), name='company-update'),
    url(r'company/delete/(?P<pk>[\d]+)/$', CompanyDelete.as_view(), name='company-delete'),
    url(r'company/$', CompanyList.as_view(), name='company-index'),

    url(r'create/$', Create.as_view(), name='create'),
    url(r'toggle_active/(?P<pk>[\d]+)/$', 'toggle_active', name='toggle-active'),
    url(r'update/(?P<pk>[\d]+)/$', Update.as_view(), name='update'),
    url(r'delete/(?P<pk>[\d]+)/$', Delete.as_view(), name='delete'),
    url(r'^$', List.as_view(), name='index'),

)
