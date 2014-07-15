# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns(
    'module.static_page.views',
    url(r'(?P<slug>.*).html$', 'entry', name='entry'),
)
