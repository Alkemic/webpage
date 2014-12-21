# -*- coding: utf-8 -*-
from smtplib import SMTPException

from django.contrib import messages
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from dc.settings import ADMINS
from boski.mixins import BreadcrumbsMixin
from module.static_page.models import Entry
from .forms import MailForm


class Index(BreadcrumbsMixin, FormView):
    """
    Displays about page (from static_page) and contact form
    """

    template_name = 'about/index.html'
    breadcrumbs = ((_('About'), reverse_lazy('about:index')),)
    form_class = MailForm
    success_url = reverse_lazy('about:index')

    def get_context_data(self, **kwargs):
        """
        Injects about page
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        context = super(Index, self).get_context_data(**kwargs)

        about_page, created = Entry.objects.get_or_create(slug='about')
        if created:
            about_page.title = 'About'
            about_page.save()

        context['about_page'] = about_page

        return context

    def form_invalid(self, form):
        messages.error(self.request, _('Please check contact form'))
        return super(Index, self).form_invalid(form)

    def form_valid(self, form):
        """
        Saving and sending email
        @param form:
        @return:
        """
        mail_entry = form.save(commit=False)
        mail_entry.ua = self.request.META['HTTP_USER_AGENT']
        mail_entry.ip = self.request.META['REMOTE_ADDR']
        mail_entry.save()

        # sending email
        try:
            email = EmailMessage(
                mail_entry.subject,
                mail_entry.content,
                '%s <%s>' % (mail_entry.author, mail_entry.email),
                [a[1] for a in ADMINS],
                headers={
                    'Reply-To': '%s <%s>' % (
                        mail_entry.author,
                        mail_entry.email,
                    ),
                }
            )
            email.send(fail_silently=False)
        except SMTPException:
            messages.error(
                self.request,
                _('An error occurred during sending email'),
            )

            return super(Index, self).form_invalid(form)
        else:
            messages.success(self.request, _('Mail has been sent'))

        return super(Index, self).form_valid(form)
