# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _

from boski.mixins import BreadcrumbsMixin

from module.blog.models import Entry


class BlogList(BreadcrumbsMixin, ListView):
    """
    Displays index page of blog
    """
    template_name = 'blog/index.html'
    context_object_name = 'list'
    queryset = Entry.objects.published()
    paginate_by = 10
    breadcrumbs = ((_('Blog'), reverse_lazy('blog:index')),)

    def dispatch(self, request, *args, **kwargs):
        return super(BlogList, self).dispatch(request, *args, **kwargs)


class TagBlogList(BreadcrumbsMixin, ListView):
    """
    Displays entries tag by given tag
    """
    template_name = 'blog/index.html'
    context_object_name = 'list'
    paginate_by = 10

    @property
    def breadcrumbs(self):
        return (_('Blog'), reverse_lazy('blog:index')), \
               (
                   _('Tag: %s') % self.kwargs['tag'],
                   reverse_lazy('blog:tag', args=[self.kwargs['tag']])
               ),

    def get_queryset(self):
        return Entry.objects.published().filter(tags__name=self.kwargs['tag'])


class EntryView(BreadcrumbsMixin, DetailView):
    """
    Display single entry
    """
    template_name = 'blog/entry.html'
    context_object_name = 'entry'
    queryset = Entry.objects.published()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            self.queryset = Entry.objects.all()
        else:
            self.queryset = Entry.objects.published()

        return super(EntryView, self).dispatch(request, *args, **kwargs)


    @property
    def breadcrumbs(self):
        if not hasattr(self, 'object') or self.object is None:
            self.object = self.get_object()

        return ((_('Blog'), reverse_lazy('blog:index')),
                ('%s' % self.object, self.object.get_absolute_url()),)
