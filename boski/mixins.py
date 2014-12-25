# -*- coding: utf-8 -*-
import simplejson
import datetime

from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class BreadcrumbsMixin(object):
    """ Mixin that pass breadcrumbs to request """
    breadcrumbs = {}

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs = self.breadcrumbs
        return super(BreadcrumbsMixin, self).dispatch(request, *args, **kwargs)


class JSONResponseMixin(object):
    def render_to_response(self, context):
        """ Returns a JSON response containing 'context' as payload """
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        """ Construct an `HttpResponse` object. """
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
        dthandler = lambda obj: obj.__str__() \
            if isinstance(obj, datetime.datetime) \
            else None
        return simplejson.dumps(context, default=dthandler)


class LoginRequiredMixin(object):
    """ Mixin class, that decorates dispatch to force login """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """ dispatch """
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
