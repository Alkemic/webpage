# -*- coding: utf-8 -*-

from django.conf import settings


def google_site_verification(request):
    site_verification = settings.__getattr__('GOOGLE_SITE_VERIFICATION')
    return {'google_site_verification': site_verification}
