# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views import IndexView, Log, Login, Logout


urlpatterns = patterns(
    'module.cms.views',
    (r'^blog/', include('module.blog.cms.urls', namespace='blog')),
    (r'^static_page/', include('module.static_page.cms.urls', namespace='static_page')),
    (r'^portfolio/', include('module.portfolio.cms.urls', namespace='portfolio')),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'log/$', Log.as_view(), name='log'),
    url(r'change_password/$', 'change_password', name='change-password'),
    url(r'login/$', Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),
)
