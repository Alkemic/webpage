#-*- coding:utf-8 -*-
from django.conf.urls import *
from django.views.decorators.cache import cache_page
from .views import Index

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

urlpatterns = patterns('',
    url(r'^$', cache_page(60*60*24)(Index.as_view()), name='index'),
)
