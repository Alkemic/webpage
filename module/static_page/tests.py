# -*- coding:utf-8 -*-
from datetime import datetime

from django.test import TestCase
from django.test.client import Client

from module.static_page.models import Entry


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

    def test_four_oh_four(self):
        response = self.client.get('/this-is-not-the-page-you-are-looking-for.html')
        self.assertEqual(404, response.status_code)


class ModelTestCase(TestCase):
    fixtures = ['static_page_testdata']

    def test_create_entry(self):
        entry = Entry(
            title="Test entry",
            content="Test content",
        )
        entry.tags = ['test', 'asd123']
        entry.save()

        entry = Entry.objects.get(title="Test entry")
        self.assertEqual('test-entry', entry.slug)

        entry.activated_at = datetime.now()
        entry.save()

    def test_select_active(self):
        active_entries = Entry.objects.active()

        self.assertEqual(active_entries.count(), 6)

        entry_about = Entry.objects.active(pk=5)
        entry_resume = Entry.objects.active(slug='resume')

        self.assertIsInstance(entry_about, Entry)
        self.assertIsInstance(entry_resume, Entry)

    def test_str_unicode(self):
        entry_about = Entry.objects.active(pk=5)
        entry_resume = Entry.objects.active(slug='resume')

        self.assertEqual(entry_resume.__str__(), u"R\xe9sum\xe9")
        self.assertEqual(unicode(entry_resume), u"Résumé")

        self.assertEqual(entry_resume.__str__(), u"R\xe9sum\xe9")

        self.assertIsInstance(entry_about.__str__(), unicode)
        self.assertIsInstance(entry_about.__unicode__(), unicode)

        self.assertEqual(str(entry_about), "About")
        self.assertEqual(unicode(entry_about), "About")

    def test_creation_and_activation(self):
        entry = Entry(
            title="Test entry",
            content="Test content",
        )

        entry.save()

        self.assertIsNone(entry.activated_at)
        entry.do_activate()
        self.assertIsNotNone(entry.activated_at)
        self.assertIsInstance(entry.activated_at, datetime)

    def test_deletion_and_un_deletion(self):
        entry = Entry(
            title="Test entry",
            content="Test content",
        )

        entry.save()

        self.assertIsNone(entry.deleted_at)
        entry.do_delete()
        self.assertIsNotNone(entry.deleted_at)
        self.assertIsInstance(entry.deleted_at, datetime)

        entry.do_undelete()
        self.assertIsNone(entry.deleted_at)
