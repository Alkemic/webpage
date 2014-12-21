# -*- coding:utf-8 -*-
import os
from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

#from dc.settings import PROJECT_ROOT

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))


@override_settings(IS_WIP=True)
class NoIndexRedirecTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_redirection(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        with open("%s/templates/wip.txt" % PROJECT_ROOT) as fh:
            contents = fh.read()
        self.assertEqual(response.content, contents)


@override_settings(IS_WIP=False)
class IndexRedirectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('blog:index')

    def test_index_redirection(self):
        response = self.client.get('/')

        self.assertRedirects(response, self.list_url, 301, 200)
