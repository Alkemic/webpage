#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from postmarkup import render_bbcode

from uuslug import uuslug as slugify

from module.static_page.managers import PublishedManager


class Entry(models.Model):
    title = models.CharField('Tytuł', max_length=255)
    slug = models.CharField('Slug', max_length=255, unique=True, db_index=True, blank=True,
                            help_text='Jeśli puste zostanie wygenerowany na podstawie tytułu. /p/&lt;slug&gt;.html')
    content = models.TextField('Treść',
                               help_text='Można korzystać z formatowania BBCode, pełna lista znaczników znajduje się <a href="/p/bbcode.html">tutaj</a>.')
    content_r = models.TextField('Wyrenderowana treść.', blank=True)

    created_at = models.DateTimeField('Data utworzenia', default=datetime.now())
    modified_at = models.DateTimeField('Data modyfikacji', default=None, blank=True, null=True)
    activated_at = models.DateTimeField('Data aktywacji', default=None, blank=True, null=True)
    deleted_at = models.DateTimeField('Data usunięcie', default=None, blank=True, null=True)

    tags = TaggableManager(_('Tags'), blank=True, related_name='has_static_pages')

    objects = PublishedManager()

    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return 'static_page:entry', [self.slug]

    def do_delete(self):
        self.deleted_at = datetime.now()

        self.save()

    def do_undelete(self):
        self.deleted_at = None

        self.save()

    def do_activate(self):
        self.activated_at = datetime.now()

        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.content_r = render_bbcode(self.content)

        if not self.slug:
            self.slug = slugify(self.title, instance=self)

        if self.pk:
            self.modified_at = datetime.now()
        else:
            self.created_at = datetime.now()

        super(Entry, self).save(force_insert, force_update, using, update_fields)

