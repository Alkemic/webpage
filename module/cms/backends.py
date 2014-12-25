# -*- coding:utf-8 -*-
"""Auth backend to allow login using email"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class ModelBackendByEmail(ModelBackend):
    """Backend that allow login with email"""
    def authenticate(self, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None and email is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel._default_manager.get(email=email)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
