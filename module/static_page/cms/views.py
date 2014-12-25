# -*- coding: utf-8 -*-
"""CMS view for static pages"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from boski.mixins import LoginRequiredMixin
from boski.views.crud import ListView, CreateView
from boski.decorators import with_template
from module.static_page.models import Entry
from module.static_page.cms.forms import EntryForm


class List(ListView, LoginRequiredMixin):
    breadcrumbs = (
        {'name': _('Static pages'), 'url': 'cms:static_page:index'},
    )

    queryset = Entry.objects.non_deleted()

    listingColumns = (
        ('id', '#'),
        ('title', _('Title')),
        ('created_at', _('Created')),
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
        })
    )

    mapColumns = {
        'id': '_displayAsIs',
        'title': '_displayEditLink',
        'created_by': '_displayAsIs',
        'created_at': '_displayDate',
        'action': '_displayStaticActionLink',
    }

    orderingColumns = {'id', 'title', 'created_at'}

    def get_fields_name(self):
        fields_name = super(List, self).get_fields_name()
        return fields_name + ['activated_at', 'slug']


class Create(LoginRequiredMixin, CreateView):
    form_class = EntryForm
    model = Entry

    @property
    def breadcrumbs(self):
        return (
            {'name': _('Static page'), 'url': 'cms:static_page:index'},
            {
                'name': self.name,
                'url': 'cms:static_page:update',
                'pk': self.get_object().pk
            },
        )


class Update(LoginRequiredMixin, CreateView):
    form_class = EntryForm
    model = Entry

    @property
    def breadcrumbs(self):
        return (
            {'name': _('Static page'), 'url': 'cms:static_page:index'},
            {
                'name': self.name,
                'url': 'cms:static_page:update',
                'pk': self.get_object().pk,
            },
        )


@login_required
@with_template('crud/create.html')
def create(request):
    form = EntryForm(request.POST or None)

    if form.is_valid():
        entry = form.save(commit=False)
        """:type : Entry """
        entry.save()
        messages.success(request, _('New static page has been created'))

        return HttpResponseRedirect(reverse('cms:static_page:index'))

    name = _('Create')
    request.breadcrumbs = (
        {'name': _('Static page'), 'url': 'cms:static_page:index'},
        {'name': name, 'url': 'cms:static_page:create'},
    )

    actions = {
        'create': 'create',
        'update': 'update',
        'delete': 'delete',
        'index': 'index',
    }

    return locals()


@login_required
@with_template('crud/update.html')
def update(request, pk):
    entry = Entry.objects.get(pk=pk)

    form = EntryForm(request.POST or None, instance=entry)

    if form.is_valid():
        entry = form.save(commit=False)
        """ :type : Entry """
        entry.save()
        messages.success(
            request, _('Successfully updated static page "%s".') % entry)

        if request.POST.get('next', None) == 'edit':
            return HttpResponseRedirect(reverse(
                'cms:static_page:update', args=[pk]
            ))

        return HttpResponseRedirect(reverse('cms:static_page:index'))

    name = _('Edit entry "%s"') % entry
    request.breadcrumbs = (
        {'name': _('Static page'), 'url': 'cms:static_page:index'},
        {'name': name, 'url': 'cms:static_page:update', 'pk': entry.pk},
    )

    actions = {
        'create': 'create',
        'update': 'update',
        'delete': 'delete',
        'index': 'index',
    }

    return dict(locals().items() + {'object': entry}.items())


@login_required
@with_template('crud/delete.html')
def delete(request, pk):
    entry = Entry.objects.get(pk=pk)

    if request.POST:
        entry.do_delete()
        messages.success(
            request, _('Static page "%s" has been deleted') % entry)
        return HttpResponseRedirect(reverse('cms:static_page:index'))

    name = _('Delete entry "%s"') % entry
    request.breadcrumbs = (
        {'name': _('Static page'), 'url': 'cms:static_page:index'},
        {'name': name, 'url': 'cms:static_page:delete', 'pk': entry.pk},
    )

    actions = {
        'create': 'create',
        'update': 'update',
        'delete': 'delete',
        'index': 'index',
    }

    return dict(locals().items() + {'object': entry}.items())


@login_required
def activate(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
        """ :type : Entry """
        entry.do_activate()
        messages.success(
            request, _(u'Static page "%s" has been activated') % entry)
    except Exception:
        messages.error(request, _('Error occurred during saving'))

    return HttpResponseRedirect(reverse('cms:static_page:index'))
