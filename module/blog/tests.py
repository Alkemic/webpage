# -*- coding:utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from module.blog.models import Entry


class ViewsTestCase(TestCase):
    fixtures = ['blog_testdata']

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('blog:index')

    def test_blog_index(self):
        """Blog index page"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        self.assertInHTML(
            '<ol class="breadcrumb"><li><a href="/"><i class="glyphicon '
            'glyphicon-home"></i></a></li><li class="active"><a href="/blog/">'
            'Blog</a></li></ol>',
            response.content
        )

    def test_index(self):
        """Test redirect from / to blog index"""
        response = self.client.get('/')

        self.assertRedirects(response, self.list_url, 301, 200)

    def test_single_entry(self):
        """Single entry"""
        test_entry = Entry.objects.published()[12]
        response = self.client.get(
            reverse('blog:entry', args=[test_entry.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            '<div class="page-header"><h2>%s</h2></div>'
                % test_entry.title.upper(),
            response.content
        )

    def test_empty_tag(self):
        """Should return empty page"""
        response = self.client.get(reverse('blog:tag', args=['test_asdasd']))

        self.assertInHTML('<div class="blog"></div>', response.content)


class ModelTestCase(TestCase):
    fixtures = ['blog_testdata']

    def test_fetch_count(self):
        self.assertEqual(Entry.objects.all().count(), 148)
        self.assertEqual(Entry.objects.deleted().count(), 0)
        self.assertEqual(Entry.objects.non_deleted().count(), 148)
        self.assertEqual(Entry.objects.published().count(), 73)

        Entry.objects.filter(id__in=range(23, 44)) \
            .update(deleted_at=datetime.now())

        self.assertEqual(Entry.objects.deleted().count(), 21)
        self.assertEqual(Entry.objects.non_deleted().count(), 127)

    def test_create(self):
        entry = Entry(
            title="Test entry",
            content="Test content",
        )
        entry.save()
        
        self.assertEqual(entry.slug, "test-entry")
        self.assertEqual(Entry.objects.all().count(), 149)
      
    def test_prev_next(self):
        all_entries = Entry.objects.published().order_by('created_at')
        first_entry = all_entries[0]
        last_entry = all_entries[all_entries.count()-1]
        
        middle_entry = all_entries[4]
        
        self.assertIsNone(first_entry.get_prev_post())
        self.assertIsNone(last_entry.get_next_post())

        middle_next = middle_entry.get_next_post()
        middle_prev = middle_entry.get_prev_post()

        self.assertIsNotNone(middle_next)
        self.assertIsNotNone(middle_prev)

        self.assertIsInstance(middle_next, Entry)
        self.assertIsInstance(middle_prev, Entry)

    def test_get_cms_link(self):
        entry = Entry.objects.get(pk=4)
        
        self.assertEqual(
            entry.get_cms_url(),
            reverse('cms:blog:update', args=[4,]),
        )
        
    def test_save(self):
        entry = Entry(
            title="Test entry",
            content="Test content",
        )
        entry.save()
        
        self.assertIsNone(entry.modified_at)
        entry.save()
        self.assertIsNotNone(entry.modified_at)
        self.assertIsInstance(entry.modified_at, datetime)

    def test_get_by_slug(self):
        entry = Entry.objects.non_deleted(slug="lorem-ipsum-dolor-sit-amet-consectetur-2")
        self.assertIsInstance(entry, Entry)
        self.assertEqual(entry.slug, "lorem-ipsum-dolor-sit-amet-consectetur-2")
        self.assertIsNone(entry.deleted_at)
        
        entry.deleted_at = datetime.now()
        entry.save()
        
        entry = Entry.objects.deleted(slug="lorem-ipsum-dolor-sit-amet-consectetur-2")
        self.assertIsInstance(entry, Entry)
        self.assertEqual(entry.slug, "lorem-ipsum-dolor-sit-amet-consectetur-2")
        self.assertIsNotNone(entry.deleted_at)
        self.assertIsInstance(entry.deleted_at, datetime)
        
        entry = Entry.objects.published(slug="lorem-ipsum-dolor-sit-amet-consectetur-8")
        self.assertIsInstance(entry, Entry)
        self.assertEqual(entry.slug, "lorem-ipsum-dolor-sit-amet-consectetur-8")
        self.assertIsNone(entry.deleted_at)
