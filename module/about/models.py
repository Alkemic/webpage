# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Mail(models.Model):
    """ Email sent from site """
    subject = models.CharField(_('Subject'), max_length=255)
    author = models.CharField(_('Author'), max_length=255)
    email = models.EmailField(_('Email'), max_length=255)
    content = models.TextField(_('Content'))

    ip = models.IPAddressField(_('IP'))
    ua = models.CharField(_('User agent'), max_length=255)

    created_at = models.DateTimeField(_('Date created'), default=datetime.now())

    class Meta:
        verbose_name = _('Mail')
        verbose_name_plural = _('Mails')
        ordering = ['-created_at', ]

    def __str__(self):
        return "%s (%s)" % (self.author, self.email)

    def __unicode__(self):
        return "%s (%s)" % (self.author, self.email)
