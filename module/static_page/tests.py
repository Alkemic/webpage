# -*- coding:utf-8 -*-
from django.test import TestCase
from django.test.client import Client


class StaticPageTestCase(TestCase):
    fixtures = ['static_page_testdata']

    def setUp(self):
        self.client = Client()

    def test_static_page(self):
        """Static page returns status code 200"""
        response = self.client.get('/resume.html')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/test-code.html')
        self.assertEqual(200, response.status_code)
