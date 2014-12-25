# -*- coding: utf-8 -*-
"""Command to fill up database with random data"""
__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'

import random
from datetime import timedelta
from random import getrandbits

from django.utils import timezone
from django.contrib.webdesign import lorem_ipsum as lipsum
from django.core.management.base import BaseCommand

from module.blog.models import Entry


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in xrange(74):
            title = lipsum.words(random.randint(1, 6))
            entry = Entry(
                title=title,
                teaser="\n".join(lipsum.paragraphs(random.randint(1, 3))),
                content="\n".join(lipsum.paragraphs(random.randint(12, 16))),
                created_at=timezone.now() - timedelta(
                    seconds=random.randint(0, 40000000)
                ),
                is_active=not getrandbits(1)
            )

            entry.save()
