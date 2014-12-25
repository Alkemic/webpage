# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _, string_concat
from module.static_page.models import Entry


def add_required_to_label(cls, class_name='required'):
    """
    @type cls: forms.BaseModelForm()
    @type class_name: str
    """
    for field_name in cls.base_fields:
        field = cls.base_fields.get(field_name, None)
        """ :type : django.forms.fields.Field """
        if field.required:
            label = field.__getattribute__('label').__str__()

            field.__setattr__('label', string_concat(label, ' *:'))

    return cls


class EntryForm(forms.ModelForm):
    """Basic form for new entries"""
    title = forms.CharField(
        label=_('Title'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Enter title')}),
    )
    content = forms.CharField(
        label=_('Content'),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Enter content'),
            'rows': '20', 'cols': '40',
        })
    )

    class Meta:
        model = Entry
        fields = ('title', 'content')
