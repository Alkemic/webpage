# -*- coding: utf-8 -*-
"""
Code (for class-based views) that helps with managing data
"""

import datetime
from math import ceil

from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView as DjangoCreateView, UpdateView as DjangoUpdateView, \
    DeleteView as DjangoDeleteView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View
from django.forms.models import model_to_dict
from django.db.models import Q
from django import http
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages

from boski.helpers import get_params
from boski.mixins import JSONResponseMixin, BreadcrumbsMixin


__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class ListView(BreadcrumbsMixin, JSONResponseMixin,
               TemplateResponseMixin, View):
    """ Basic listing with AJAX data loading """
    template_name = 'crud/list.html'
    queryset = None

    name = _('Entries list')

    listingColumns = ()
    filters = ()
    mapColumns = {}
    orderingColumns = {}
    searchColumns = {}
    actions = {
        'create': 'create',
        'update': 'update',
        'delete': 'delete',
        'index': 'index',
    }

    allow_create = True
    allow_update = True
    allow_delete = True

    per_page = 30

    def get(self, request, *args, **kwargs):
        json_required = any((
            self.request.is_ajax(),
            self.request.GET.get('format', 'html') == 'json',
        ))
        if json_required:
            context = self.get_context_ajax()
            return JSONResponseMixin.render_to_response(self, context)
        else:
            context = self.get_context_data()
            return TemplateResponseMixin.render_to_response(self, context)

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

    def get_context_data(self):
        return {
            'filters': self.filters,
            'per_page': self.per_page,
            'orderingColumns': self.orderingColumns,
            'mapColumns': self.mapColumns,
            'searchColumns': self.searchColumns,
            'listingColumns': self.listingColumns,
            'actions': self.actions,
            'name': self.name,
            'allow_create': self.allow_create,
            'allow_update': self.allow_update,
            'allow_delete': self.allow_delete,
        }

    def get_context_ajax(self):
        params = get_params(self.request)

        phrase = params.get('phrase', None)
        ordering = params.get('ordering', '-id')
        where = params.get('where', False)

        try:
            page = int(params.get('page', 1))
        except ValueError:
            page = 1

        listing = self.do_search(phrase, where, ordering)
        items_count = listing.count()

        pages = int(ceil(float(items_count) / float(self.per_page)))
        page = pages if page > pages else page
        page = 1 if page < 1 else page
        offset = (page - 1) * self.per_page
        listing = listing[offset:offset + self.per_page]

        response_dict = {
            'data': self.prepare_response_data(listing),
            '_meta': {
                'canAdd': True,
                'canEdit': True,
                'canDelete': True,
                'items': items_count,
                'pages': ceil(items_count / self.per_page),
                'currentPage': page,
            },
            '_params': params
        }

        return response_dict

    def do_search(self, phrase=None, where=None, ordering=None):
        """ Filtering query_set by phrase, where and do ordering """
        listing = self.queryset

        if ordering is not None:
            listing = listing.order_by(ordering)

        if where:
            listing = listing.filter(self.prepare_where_statement(where))

        if phrase:
            listing = listing.filter(self.prepare_phrase_statement(phrase))

        return listing

    def prepare_response_data(self, data):
        """ Dumps QuerySet into dict """
        response_data = {}

        fields_name = self.get_fields_name()
        i = 0
        for row in data:
            response_data[i] = model_to_dict(
                row, fields=fields_name, exclude=[])
            response_data[i]['_meta'] = {}
            i += 1

        return response_data

    def get_fields_name(self):
        """ Returns keys by witch we will be returning data to view """
        return [field for field, name in self.listingColumns]

    def prepare_phrase_statement(self, phrase):
        statement = None

        if not self.searchColumns:
            return Q(pk__isnull=True)

        for col_name in self.searchColumns:
            statement = Q(**{col_name + '__icontains': phrase}) \
                if statement is None \
                else statement | Q(**{col_name + '__icontains': phrase})

        return statement

    def prepare_where_statement(self, where):
        where_statement = None

        for col_name in where:
            if col_name.__contains__('_at'):
                value = datetime.datetime.strptime(where[col_name], '%Y-%m-%d')
                value = datetime.date(value.year, value.month, value.day)
            else:
                value = where[col_name]

            where_statement = Q(**{col_name: value}) \
                if where_statement is None \
                else where_statement | Q(**{col_name: value})

        return where_statement


class UpdateView(BreadcrumbsMixin, DjangoUpdateView):
    template_name = 'crud/update.html'
    model = None
    fields = []
    actions = ListView.actions

    @property
    def name(self):
        return _('Edit entry "%s"') % self.get_object()

    def get_object(self, queryset=None):
        if not hasattr(self, '_object') or self._object is None:
            obj = super(UpdateView, self).get_object(queryset)
            self._object = obj

        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['actions'] = self.actions
        context['name'] = self.name
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, _('Changes has been saved'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        resolved = resolve(self.request.path)
        if self.request.POST.get('next', None) == 'edit':
            return reverse('%s:%s' % (
                resolved.namespace, self.actions['update']
            ), kwargs={'pk': self.object.pk})
        else:
            return reverse('%s:%s' % (
                resolved.namespace, self.actions['index']))


class CreateView(BreadcrumbsMixin, DjangoCreateView):
    template_name = 'crud/create.html'
    model = None
    fields = []
    actions = ListView.actions
    object = None

    name = _('Create entry')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, _('New entry has been created'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['actions'] = self.actions
        context['name'] = self.name
        return context

    def get_success_url(self):
        r = resolve(self.request.path)
        if self.request.POST.get('next', None) == 'edit':
            return reverse('%s:%s' % (
                r.namespace, self.actions['update']
            ), kwargs={'pk': self.object.pk})
        else:
            return reverse('%s:%s' % (r.namespace, self.actions['index']))


class DeleteView(BreadcrumbsMixin, DjangoDeleteView):
    template_name = 'crud/delete.html'
    model = None
    actions = ListView.actions

    @property
    def name(self):
        return _('Delete entry "%s"') % self.get_object()

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        context['name'] = self.name
        context['actions'] = self.actions
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.deleted_at = datetime.datetime.now()
            self.object.save()

            messages.success(request, _('Entry has been deleted'))
            return http.HttpResponseRedirect(success_url)
        except:
            messages.error(request, _('An error has occurred'))

    def get_success_url(self):
        r = resolve(self.request.path)
        return reverse('%s:%s' % (r.namespace, self.actions['index']))
