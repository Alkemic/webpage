# -*- coding: utf-8 -*-
"""Cms portfolio views"""
from datetime import datetime

from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from boski.views.crud import ListView, CreateView, UpdateView, DeleteView
from boski.mixins import LoginRequiredMixin
from ..models import Entry, Company
from .forms import EntryForm, CompanyForm


__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class List(LoginRequiredMixin, ListView):
    queryset = Entry.objects.all().filter(deleted_at__isnull=True)

    breadcrumbs = ({'name': _('Portfolio'), 'url': 'cms:portfolio:index'},)

    listingColumns = (
        ('id', '#'),
        ('name', _('Name')),
        ('created_at', _('Date created')),
        ('action', _('Actions'))
    )

    filters = (
        ('created_at__gte', {
            'label': _('Created from'),
            'type': 'text',
            'class': 'calendar',
        }),
        ('created_at__lte', {
            'label': _('To'),
            'type': 'text',
            'class': 'calendar',
        }),
    )

    mapColumns = {
        'id': '_displayAsIs',
        'name': '_displayEditLink',
        'created_at': '_displayDate',
        'action': '_displayActionWithActivationToggleLink',
    }

    def get_fields_name(self):
        fields_name = super(List, self).get_fields_name()
        return fields_name + ['activated_at', 'slug']

    orderingColumns = {'id', 'name', 'created_at'}

    searchColumns = {'name', 'description', 'technologies'}


class Create(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': self.name, 'url': 'cms:portfolio:create'}


class Update(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': self.name, 'url': 'cms:portfolio:update',
                'pk': self.get_object().pk}


class Delete(LoginRequiredMixin, DeleteView):
    model = Entry

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': self.name, 'url': 'cms:portfolio:delete',
                'pk': self.get_object().pk}


@login_required
def toggle_active(request, pk):
    entry = Entry.objects.non_deleted().get(pk=pk)
    """ :type : Entry """

    if entry.activated_at:
        try:
            entry.activated_at = False
            entry.save()
            messages.success(request, _('Entry has been deactivated'))
        except:
            messages.error(request, _('Error occurred during saving'))
    else:
        try:
            entry.activated_at = datetime.now()
            entry.save()
            messages.success(request, _('Entry has been activated'))
        except:
            messages.error(request, _('Error occurred during saving'))

    return HttpResponseRedirect(reverse('cms:portfolio:index'))


class CompanyList(LoginRequiredMixin, ListView):
    queryset = Company.objects.all()

    breadcrumbs = (
        {'name': _('Portfolio'), 'url': 'cms:portfolio:index'},
        {'name': _('Company'), 'url': 'cms:portfolio:company-index'},
    )

    listingColumns = (
        ('id', '#'),
        ('name', _('Name')),
        ('created_at', _('Date created')),
        ('action', _('Actions'))
    )

    mapColumns = {
        'id': '_displayAsIs',
        'name': '_displayEditLink',
        'created_at': '_displayDate',
        'action': '_displayActionLink',
    }

    actions = {
        'create': 'company-create',
        'update': 'company-update',
        'delete': 'company-delete',
        'index': 'company-index',
    }

    orderingColumns = {'id', 'name', 'created_at'}

    searchColumns = {'name', 'teaser', 'content'}


class CompanyCreate(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    actions = CompanyList.actions

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': _('Company'), 'url': 'cms:portfolio:company-index'}, \
               {'name': self.name, 'url': 'cms:portfolio:company-create'}


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    actions = CompanyList.actions

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': _('Company'), 'url': 'cms:portfolio:company-index'}, \
               {'name': self.name, 'url': 'cms:portfolio:company-update',
                'pk': self.get_object().pk}


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    actions = CompanyList.actions

    @property
    def breadcrumbs(self):
        return {'name': _('Portfolio'), 'url': 'cms:portfolio:index'}, \
               {'name': _('Company'), 'url': 'cms:portfolio:company-index'}, \
               {'name': self.name, 'url': 'cms:portfolio:company-delete',
                'pk': self.get_object().pk}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()

            messages.success(request, _('Entry has been deleted'))
            return http.HttpResponseRedirect(success_url)
        except:
            messages.error(request, _('An error has occurred'))
