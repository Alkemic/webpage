# -*- coding: utf-8 -*-
from django import forms

from .models import Mail


__author__ = 'Daniel Alkemic Czuba <alkemic7@gmail.com>'


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['subject', 'author', 'email', 'content']
