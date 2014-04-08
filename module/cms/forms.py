# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

__author__ = 'Daniel Alkemic Czuba <alkemic7@gmail.com>'


class LoginForm(forms.Form):
    """Formularz rejestracji."""
    # username = forms.CharField(label='Login', min_length=3, max_length=90)
    email = forms.CharField(label='Email', min_length=3, max_length=90)
    password = forms.CharField(label='Hasło', min_length=6, widget=forms.PasswordInput)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_('New password'), min_length=6, widget=forms.PasswordInput,
                                    help_text=_('At least 6 chars'))
    new_password2 = forms.CharField(label=_('Repeat new password'), min_length=6, widget=forms.PasswordInput,
                                    help_text=_('At least 6 chars'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("Passwords doesn't match"))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Twoje stare hasło jest niepoprawne. Wprowadź je ponownie.")
        return old_password


PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']


