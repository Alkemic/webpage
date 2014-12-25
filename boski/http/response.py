# -*- coding: utf-8 -*-
import json
import datetime

from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.http.response import HttpResponse


__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class HttpResponseAjax(HttpResponse):
    """
    Class that automagicly serialize content into JSON.
    """

    def __init__(self, content=b'', *args, **kwargs):
        def json_handler(obj):
            if isinstance(obj, datetime.datetime):
                return obj.__str__()
            elif isinstance(obj, Promise):
                return force_unicode(obj)

            return None

        content = b'%s' % json.dumps(content, default=json_handler)
        super(HttpResponseAjax, self).__init__(content, *args, **kwargs)
