#-*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from boski.decorators import with_template

from .models import Entry, Company


@with_template
def index(request):
    entries = Entry.objects.filter(deleted_at__isnull=True).order_by('company', '-from_date')
    """ :type : list of Entry """
    companies = Company.objects.all()
    """ :type : list of Company """

    request.breadcrumbs = ((_('Portfolio'), reverse('portfolio:index')),)

    return locals()
