# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from module.static_page.models import Entry
from module.about.models import Mail


class ViewsTestCase(TestCase):
    fixtures = ['static_page_testdata']

    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about:index')

    def test_get(self):
        """About page returns status code 200"""
        response = self.client.get(self.about_url)

        self.assertEqual(response.status_code, 200)

        self.assertInHTML(
            '<div class="page-header"><h2>About</h2></div>',
            response.content
        )

    def test_form_invalid(self):
        response = self.client.post(
            self.about_url,
            {},
            HTTP_USER_AGENT='Mozilla/5.0',
        )

        self.assertEqual(response.status_code, 200)

        self.assertInHTML(
            '<div class="alert alert-danger alert-dismissable"><button '
            'type="button" class="close" data-dismiss="alert" aria-hidden='
            '"true">&#215;</button>Please check contact form</div>',
            response.content
        )

    def test_form_valid(self):
        """About page returns status code 200"""
        form_data = {
            'subject': 'Test subject',
            'author': 'Test author', 'email':
            'test@example.net',
            'content': 'Test content',
        }

        response = self.client.post(
            self.about_url,
            form_data,
            HTTP_USER_AGENT='Mozilla/5.0',
        )

        self.assertRedirects(response, self.about_url, 302, 200)

    def test_about_auto_create(self):
        """Creation of about page"""
        Entry.objects.get(title='About').delete()

        response = self.client.get(self.about_url)

        self.assertEqual(200, response.status_code)
        self.assertInHTML(
            '<div class="page-header"><h2>About</h2></div>',
            response.content,
        )


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class FailedViewsTestCase(TestCase):
    fixtures = ['static_page_testdata']

    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about:index')

    def test_invlid_mail_send(self):
        """Emulate problem with sending email"""
        form_data = {
            'subject': 'Test subject',
            'author': 'Test author', 'email':
            'test@example.net',
            'content': 'Test content',
        }

        response = self.client.post(
            self.about_url,
            form_data,
            HTTP_USER_AGENT='Mozilla/5.0',
        )

        self.assertEqual(200, response.status_code)

        self.assertInHTML(
            '<div class="alert alert-danger alert-dismissable"><button '
            'type="button" class="close" data-dismiss="alert" '
            'aria-hidden="true">&#215;</button>An error occurred during '
            'sending email</div>',
            response.content
        )


class ModelTestCase(TestCase):
    fixtures = ['static_page_testdata']

    def test_str_unicode(self):
        mail = Mail(
            subject='Test mail',
            author='Test author',
            email='test@example.net',
            content='Test content',
            ip='127.0.0.1',
            ua='DjangoTestSuite',
        )
        mail.save()

        self.assertIsInstance(mail.__str__(), unicode)
        self.assertIsInstance(mail.__unicode__(), unicode)

        self.assertEqual(str(mail), "Test author (test@example.net)")
        self.assertEqual(unicode(mail), "Test author (test@example.net)")
