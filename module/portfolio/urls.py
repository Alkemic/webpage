#-*- coding:utf-8 -*-
from django.conf.urls import *

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

urlpatterns = patterns('module.portfolio.views',
    # url(r'^(?P<slug>.*).html$', EntryView.as_view(), name='entry'),
    url(r'/?$', 'index', name='index'),
)
