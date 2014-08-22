# -*- coding:utf-8 -*-
from datetime import datetime, date

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.db.models.query import QuerySet

from module.portfolio.models import Entry, Company


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


class ModelTestCase(TestCase):
    fixtures = ['portfolio_testdata']

    def test_entry_str_unicode(self):
        entry = Entry.objects.get(slug='ogradzamy-pl')

        self.assertIsInstance(entry.__str__(), unicode)
        self.assertIsInstance(entry.__unicode__(), unicode)

        self.assertEqual(str(entry), "Ogradzamy.pl")
        self.assertEqual(unicode(entry), "Ogradzamy.pl")

    def test_company_str_unicode(self):
        company = Company.objects.get(pk=1)

        self.assertIsInstance(company.__str__(), unicode)
        self.assertIsInstance(company.__unicode__(), unicode)

        self.assertEqual(str(company), "Effigo sp. z o.o.")
        self.assertEqual(unicode(company), "Effigo sp. z o.o.")

    def test_entry_save(self):
        entry = Entry(
            name='Test entry',
            company=Company.objects.all()[0],
        )

        entry.save()
        self.assertEqual(entry.slug, "test-entry")

        entry.published_at = datetime.now()
        entry.save()

    def test_company_save(self):
        company = Company(
            name='Test company',
            from_date=date.today(),
        )

        company.save()
        self.assertEqual(company.slug, "test-company")

        company.published_at = "Test description"
        company.save()

    def test_fetch_by_manager(self):
        entry = Entry.objects.non_deleted(slug='ogradzamy-pl')

        self.assertIsInstance(entry, Entry)
        self.assertIsNone(entry.deleted_at)

        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.deleted(slug='ogradzamy-pl')

        entry.deleted_at = datetime.now()
        entry.save()
        entry = Entry.objects.deleted(slug='ogradzamy-pl')

        self.assertIsInstance(entry, Entry)
        self.assertIsNotNone(entry.deleted_at)

        deleted_entries = Entry.objects.deleted()
        self.assertIsInstance(deleted_entries, QuerySet)
        self.assertEqual(deleted_entries.count(), 1)
