#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView

from boski.views.base import TemplateTextPlainView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^robots\.txt$', TemplateTextPlainView.as_view(template_name='robots.txt')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', TemplateTextPlainView.as_view(template_name='wip.txt'), name='index'),
    url(r'^$', RedirectView.as_view(pattern_name='blog:index'), name='index'),
    (r'about/', include('module.about.urls', namespace='about')),
    (r'^cms/', include('module.cms.urls', namespace='cms')),
    (r'^blog/', include('module.blog.urls', namespace='blog')),
    (r'^', include('module.static_page.urls', namespace='static_page')),
    (r'portfolio/', include('module.portfolio.urls', namespace='portfolio')),
    # url(r'^dc/', include('dc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

