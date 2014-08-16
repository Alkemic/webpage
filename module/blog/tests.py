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
