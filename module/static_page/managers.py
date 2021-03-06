# -*- coding: utf-8 -*-
from django.db.models import Manager


class PublishedManager(Manager):
    def active(self, pk=False, slug=False):
        """ Zwraca aktywne strony """
        query_set = self.non_deleted().filter(activated_at__isnull=False)
        if slug:
            return query_set.get(slug=slug)
        elif pk:
            return query_set.get(pk=pk)

        return query_set

    def non_deleted(self):
        """ Returns non deleted entries """
        return self.get_queryset().filter(deleted_at__isnull=True)
