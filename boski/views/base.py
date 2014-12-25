# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class TemplateTextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TemplateTextPlainView, self).render_to_response(
            context, content_type='text/plain', **kwargs)
