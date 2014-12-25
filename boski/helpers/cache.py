# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache import cache


def delete_view_cache(url=None, pattern=None, args=None, kwargs=None,
                      query_string=None, key_prefix=None):
    """
    Provide `url` or `pattern` (ie: 'blog:index') with `args`/`kwargs`
    When successfully delete data from cache returns True, else False. Where
    False indicates plenty of thing, ie: cache
    error, key missing, etc.

    @param url: string or None
    @param pattern: string or None
    @param args: string or None
    @param kwargs: string or None
    @param key_prefix: string or None
    @return: bool
    """

    # dummy request
    request = HttpRequest()

    request.QUERY_STRING = '' if query_string is None else query_string

    if url:
        request.path = url
    elif pattern:
        request.path = reverse(pattern, args=args, kwargs=kwargs)
    else:
        raise Exception('You must provide `url` or `pattern` argument')

    key = get_cache_key(request, key_prefix=key_prefix)

    if key and cache.get(key):
        cache.set(key, None, 0)
        return True

    return False
