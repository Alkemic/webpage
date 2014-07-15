# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from postmarkup import _postmarkup, SimpleTag, strip_bbcode as postmarkup_strip_bbcode
from postmarkup.parser import create

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

for i in xrange(1, 7):
    create.add_tag(SimpleTag, 'h%d' % i, 'h%d' % i)

for i in xrange(1, 7):
    _postmarkup.tag_factory.add_tag(SimpleTag, 'h%d' % i, 'h%d' % i)

render_bbcode = _postmarkup.render_to_html

register = template.Library()


@register.filter
def bbcode(value):
    """
    Generates (X)HTML from string with BBCode "markup".
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/
    """
    return mark_safe(render_bbcode(value))


bbcode.is_save = True


@register.filter
def strip_bbcode(value):
    """
    Strips BBCode tags from a string
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/
    """
    return mark_safe(postmarkup_strip_bbcode(value))


strip_bbcode.is_save = True
