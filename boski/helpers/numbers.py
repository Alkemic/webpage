# -*- coding: utf-8 -*-
__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


def parse_int(value, default=None):
    """
    Parse value into integer, or return default on any error
    :rtype: int
    """
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default
