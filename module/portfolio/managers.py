# -*- coding: utf-8 -*-
from django.db.models import Manager
from datetime import datetime


class PublicManager(Manager):
    """Basic manager"""

    def non_deleted(self, slug=False):
        """Returns non deleted entries"""
        if slug:
            return self.get_queryset()\
                .filter(deleted_at__isnull=True)\
                .get(slug=slug)
        else:
            return self.get_queryset()\
                .filter(deleted_at__isnull=True)

    def deleted(self, slug=False):
        """Returns deleted entries"""
        if slug:
            return self.get_queryset()\
                .filter(deleted_at__isnull=False)\
                .get(slug=slug)
        else:
            return self.get_queryset()\
                .filter(deleted_at__isnull=False)
