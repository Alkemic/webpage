#-*- coding:utf-8 -*-
from django.conf.urls import *
from django.views.decorators.cache import cache_page
from .views import BlogList, EntryView, TagBlogList

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

urlpatterns = patterns('',
    url(r'^(?P<slug>.*).html$', cache_page(60*60*24)(EntryView.as_view()), name='entry'),
    # url(r'^(?P<slug>.*).html$', EntryView.as_view(), name='entry'),
    url(r'tag/(?P<tag>.*)/$', cache_page(60*60*24)(TagBlogList.as_view()), name='tag'),
    url(r'$', cache_page(60*60*24)(BlogList.as_view()), name='index'),
)
