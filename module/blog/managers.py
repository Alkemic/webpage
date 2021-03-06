# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Manager


class PublicManager(Manager):
    """Returns published posts that are not in the future and are not
    deleted."""

    def published(self, slug=False):
        if slug:
            return self.get_queryset() \
                .filter(created_at__lte=datetime.now()) \
                .filter(deleted_at__isnull=True) \
                .filter(is_active=True) \
                .get(slug=slug)
        else:
            return self.get_queryset().filter(created_at__lte=datetime.now()) \
                .filter(deleted_at__isnull=True) \
                .filter(is_active=True)

    def non_deleted(self, slug=False):
        if slug:
            return self.get_queryset() \
                .filter(deleted_at__isnull=True) \
                .get(slug=slug)
        else:
            return self.get_queryset().filter(deleted_at__isnull=True)

    def deleted(self, slug=False):
        if slug:
            return self.get_queryset() \
                .filter(deleted_at__isnull=False) \
                .get(slug=slug)
        else:
            return self.get_queryset().filter(deleted_at__isnull=False)
