#-*- coding:utf-8 -*-
from django import forms
from django.utils.encoding import force_text, smart_text
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
        # print field.required
        if field.required:
            # print field.widget.attrs
            label = field.__getattribute__('label').__str__()
            # print dir(label)
            # print string_concat(label, 'asd')
            # print label.decode()
            # print force_text(label)
            # print "%s*" % label

            # print label.__str__()
            # field.__setattr__('label', string_concat(label, _('%s *:')))
            # field.__setattr__('label', string_concat(label, _(' *:')))
            print smart_text(label)
            field.__setattr__('label', string_concat(label, ' *:'))
            # field.__setattr__('label', _('%s *:') % label)
            # print field.widget.is_required
            """ @type field.widget: django.forms.widgets.Widget """
            # field.widget

    return cls


class EntryForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), required=True,
                            widget=forms.TextInput(attrs={'placeholder': _('Enter title')}))
    content = forms.CharField(label=_('Content'), required=True,
                              widget=forms.Textarea(
                                  attrs={'placeholder': _('Enter content'), 'rows': '20', 'cols': '40'}))

    class Meta:
        model = Entry
        fields = ('title', 'content')


# EntryForm = add_required_to_label(EntryForm)
