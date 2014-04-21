# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from boski.views.crud import ListView, CreateView, UpdateView, DeleteView
from boski.mixins import LoginRequiredMixin

from module.blog.models import Entry

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


class List(LoginRequiredMixin, ListView):
    queryset = Entry.objects.non_deleted()

    breadcrumbs = ({'name': _('Blog'), 'url': 'cms:blog:index'},)

    listingColumns = (
        ('id', '#'),
        ('title', _('Title')),
        ('created_at', _('Date created')),
        ('action', _('Actions'))
    )

    filters = (
        ('created_at__gte', {'label': _('Created from'), 'type': 'text', 'class': 'calendar'}),
        ('created_at__lte', {'label': _('To'), 'type': 'text', 'class': 'calendar'})
    )

    mapColumns = {
        'id': '_displayAsIs',
        'title': '_displayEditLink',
        'created_at': '_displayDate',
        'action': '_displayActionWithActivationToggleLink',
    }

    def get_fields_name(self):
        fields_name = super(List, self).get_fields_name()
        return fields_name+['is_active', 'slug']

    orderingColumns = {'id', 'title', 'created_at'}

    searchColumns = {'title', 'teaser', 'content'}


class Update(LoginRequiredMixin, UpdateView):
    model = Entry
    fields = ['title', 'teaser', 'content', 'tags', 'is_active']

    @property
    def breadcrumbs(self):
        return {'name': _('Blog'), 'url': 'cms:blog:index'}, \
               {'name': self.name, 'url': 'cms:blog:update', 'pk': self.get_object().pk}


class Create(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ['title', 'teaser', 'content', 'tags', 'is_active']

    @property
    def breadcrumbs(self):
        return {'name': _('Blog'), 'url': 'cms:blog:index'}, {'name': self.name, 'url': 'cms:blog:create'}


class Delete(LoginRequiredMixin, DeleteView):
    model = Entry

    @property
    def breadcrumbs(self):
        return {'name': _('Blog'), 'url': 'cms:blog:index'}, \
               {'name': self.name, 'url': 'cms:blog:delete', 'pk': self.get_object().pk}


@login_required
def toggle_active(request, pk):
    entry = Entry.objects.non_deleted().get(pk=pk)

    if entry.is_active:
        try:
            entry.is_active = False
            entry.save()
            messages.success(request, _('Entry has been deactivated'))
        except:
            messages.error(request, _('Error occurred during saving'))
    else:
        try:
            entry.is_active = True
            entry.save()
            messages.success(request, _('Entry has been activated'))
        except:
            messages.error(request, _('Error occurred during saving'))

    return HttpResponseRedirect(reverse('cms:blog:index'))
