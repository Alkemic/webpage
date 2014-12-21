# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from postmarkup.parser import (
    create,
    pygments_available,
    SimpleTag,
    ImgTag,
    strip_bbcode as postmarkup_strip_bbcode,
)

from postmarkup.parser import create

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


_postmarkup = create(
    use_pygments=pygments_available,
    annotate_links=False,
    exclude=['img'],
)

for i in xrange(1, 7):
    _postmarkup.tag_factory.add_tag(SimpleTag, 'h%d' % i, 'h%d' % i)

render_bbcode = _postmarkup.render_to_html

class BootstrapImgTag(ImgTag):
    """
    Adding bootstrap img classes
    """
    def render_open(self, parser, node_index):
        rendered = super(BootstrapImgTag, self).render_open(parser, node_index)

        rendered = rendered.replace(
            '<img ',
            '<img class="img-responsive img-thumbnail" ',
        )

        return rendered


_postmarkup.tag_factory.add_tag(BootstrapImgTag, u'img')

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
