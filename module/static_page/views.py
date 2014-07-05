# -*- coding:utf-8 -*-
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from boski.decorators import with_template
from .models import Entry


@with_template
def entry(request, slug):
    try:
        entry = Entry.objects.active(slug=slug)
        """ :type : Entry """
    except Entry.DoesNotExist:
        raise Http404(_('Request page doesn\'t exists'))

    request.breadcrumbs = (('%s' % entry, entry.get_absolute_url),)

    return locals()
