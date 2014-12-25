# -*- coding: utf-8 -*-
"""BBCode views"""
from postmarkup.parser import render_bbcode

from boski.http.response import HttpResponseAjax


def render(request):
    """Returns all fields in POST rendered"""
    response_data = {}

    for key in request.POST:
        response_data[key] = render_bbcode(request.POST[key])

    return HttpResponseAjax(response_data)
