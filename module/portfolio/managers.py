# -*- coding: utf-8 -*-
from django.db.models import Manager
from datetime import datetime

class PublicManager(Manager):
    """Returns published posts that are not in the future and are not deleted."""

    def non_deleted(self, slug=False):
        if slug:
            return self.get_query_set().filter(deleted_at__isnull=True).get(slug=slug)
        else:
            return self.get_query_set().filter(deleted_at__isnull=True)

    def deleted(self, slug=False):
        if slug:
            return self.get_query_set().filter(deleted_at__isnull=False).get(slug=slug)
        else:
            return self.get_query_set().filter(deleted_at__isnull=False)
