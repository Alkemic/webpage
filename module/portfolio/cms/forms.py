#-*- coding:utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _

from module.portfolio.models import Entry, Company


class EntryForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super(EntryForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                        empty_permitted, instance)

        if instance is not None:
            self.fields['main_photo'].required = False

    class Meta:
        model = Entry
        exclude = ('slug', 'description_html', 'created_at', 'modified_at', 'deleted_at', 'published_at')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('slug', 'description_html', 'created_at')
