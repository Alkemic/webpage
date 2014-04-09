#-*- coding:utf-8 -*-
"""
Installation specific settings.
Copy this file to settings_local.py, and fill up.
"""
from settings import PROJECT_NAME

ADMINS = (
    ('admin', 'admin@dummy-domain.com'),
)

MANAGERS = ADMINS

LOCAL_MIDDLEWARE_CLASSES = ()

LOCAL_INSTALLED_APPS = ()

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s.sqlite' % PROJECT_NAME,
        # 'NAME': 'name',
        # 'USER': 'user',
        # 'PASSWORD': 'password',
        # 'HOST': 'host',
        # 'PORT': 'port',
    }
}

GOOGLE_SITE_VERIFICATION = ''

ALLOWED_HOSTS = ['*']
