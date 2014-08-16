# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from module.static_page.models import Entry

class ViewsTestCase(TestCase):
    fixtures = ['portfolio_testdata']

    def setUp(self):
        self.client = Client()
        self.portfolio_url = reverse('portfolio:index')

    def test_get(self):
        """Portfolio index page returns status code 200"""
        response = self.client.get(self.portfolio_url)

        self.assertEqual(response.status_code, 200)

        self.assertInHTML(
            '<h3>Ogradzamy.pl</h3>',
            response.content
        )
