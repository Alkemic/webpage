# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect

from boski.views.base import TemplateTextPlainView


class IndexView(TemplateTextPlainView):
    template_name='wip.txt'

    def dispatch(self, request, *args, **kwargs):
        if not settings.IS_WIP:
            return redirect('blog:index', permanent=True)
        
        return super(IndexView, self).dispatch(request, *args, **kwargs)
