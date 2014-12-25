# -*- coding: utf-8 -*-
"""Abouts forms"""
from django import forms

from .models import Mail


class MailForm(forms.ModelForm):
    """Form used in about page"""
    class Meta:
        model = Mail
        fields = ['subject', 'author', 'email', 'content']
