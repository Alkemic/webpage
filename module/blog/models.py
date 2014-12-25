# -*- coding: utf-8 -*-
"""Models related to blog"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuslug import uuslug as slugify
from taggit.managers import TaggableManager

from module.blog.managers import *


class Entry(models.Model):
    """ Model with blog entries """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(
        _('SLUG'),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    teaser = models.TextField(_('Teaser'), blank=True, null=True)
    teaser_r = models.TextField(
        _('Rendered teaser'),
        blank=True,
        null=True,
    )
    content = models.TextField(_('Content'))
    content_r = models.TextField(_('Rendered content'), blank=True, null=True)

    is_active = models.BooleanField(_('Is active?'), default=False)

    created_at = models.DateTimeField(
        _('Date created'),
        default=datetime.now(),
    )
    modified_at = models.DateTimeField(
        _('Date modified'),
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(_('Date deleted'), blank=True, null=True)

    tags = TaggableManager(
        _('Tags'),
        blank=True,
        related_name='has_blog_entries',
    )

    objects = PublicManager()

    _prev_post = None
    _next_post = None

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ['-created_at', ]

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_next_post(self):
        if self._next_post is not None:
            return self._next_post

        try:
            # maybe it's not a good assumption, that never will be post with
            # same created_at value
            self._next_post = Entry.objects.published() \
                .filter(created_at__gt=self.created_at) \
                .order_by('created_at')[0]
        except (Entry.DoesNotExist, IndexError):
            self._next_post = None

        return self._next_post

    def get_prev_post(self):
        if self._prev_post is not None:
            return self._prev_post

        try:
            # maybe it's not a good assumption, that never will be post with
            # same created_at value
            self._prev_post = Entry.objects.published() \
                .filter(created_at__lt=self.created_at) \
                .order_by('-created_at')[0]
        except (Entry.DoesNotExist, IndexError):
            self._prev_post = None

        return self._prev_post

    @models.permalink
    def get_absolute_url(self):
        return 'blog:entry', (), {'slug': self.slug}

    @models.permalink
    def get_cms_url(self):
        return 'cms:blog:update', (), {'pk': self.id}

    def save(self, **kwargs):
        if self.pk:
            self.modified_at = datetime.now()

        if not self.slug:
            self.slug = slugify(self.title, instance=self)

        super(Entry, self).save(**kwargs)
