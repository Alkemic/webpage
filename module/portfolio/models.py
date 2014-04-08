#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from uuslug import uuslug as slugify
from postmarkup import render_bbcode


__author__ = 'Daniel Alkemic Czuba <alkemic7@gmail.com>'


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=255, blank=False, null=False)
    slug = models.SlugField(_('SLUG'), max_length=255, unique=True)

    main_photo = models.ImageField(_('Main photo'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)

    site = models.URLField(_('Site'), blank=True, null=True)
    from_date = models.DateField(_('From date'))
    to_date = models.DateField(_('To date'), blank=True, null=True)

    description = models.TextField(_('Description'), blank=False)
    description_html = models.TextField(_('Description (html)'), blank=False)

    created_at = models.DateTimeField(_('Date created'), default=datetime.now())

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['-created_at', ]

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)

        # self.teaser_html = bbcode(self.teaser)
        self.description_html = bbcode(self.description)

        super(Company, self).save(**kwargs)


class Entry(models.Model):
    """ Entries in portfolio """
    name = models.CharField(_('Name'), max_length=255, blank=False, null=False)
    slug = models.SlugField(_('SLUG'), max_length=255, unique=True)

    main_photo = models.ImageField(_('Main photo'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_1 = models.ImageField(_('Additional photo #1'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_2 = models.ImageField(_('Additional photo #2'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_3 = models.ImageField(_('Additional photo #3'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_4 = models.ImageField(_('Additional photo #4'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_5 = models.ImageField(_('Additional photo #5'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)
    photo_6 = models.ImageField(_('Additional photo #6'), upload_to='upload/%Y/%m', max_length=255, blank=True, null=True)

    description = models.TextField(_('Description'), blank=False, null=True)
    description_html = models.TextField(_('Description (html)'), blank=True)

    technologies = TaggableManager(_('Technologies'), blank=True)

    from_date = models.DateField(_('From date'), blank=True, null=True)
    to_date = models.DateField(_('To date'), blank=True, null=True)

    company = models.ForeignKey(Company, verbose_name=_('Company'), max_length=255)
    site = models.URLField(_('Site'), blank=True, null=True)
    demo = models.URLField(_('Demo'), blank=True, null=True)
    source = models.URLField(_('Source code'), blank=True, null=True)

    created_at = models.DateTimeField(_('Date created'), default=datetime.now())
    modified_at = models.DateTimeField(_('Date modified'), blank=True, null=True)

    deleted_at = models.DateTimeField(_('Date deleted'), blank=True, null=True)
    published_at = models.DateTimeField(_('Date published'), blank=True, null=True)

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if self.pk:
            self.modified_at = datetime.now()

        if not self.slug:
            self.slug = slugify(self.name, instance=self)

        # self.teaser_html = bbcode(self.teaser)
        self.description_html = render_bbcode(self.description)

        super(Entry, self).save(**kwargs)
