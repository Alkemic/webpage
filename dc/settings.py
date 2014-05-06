#-*- coding:utf-8 -*-
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
PROJECT_NAME = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1']

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl-PL'

SITE_ID = 1

USE_I18N = True

USE_L10N = False

USE_TZ = False

LOGIN_URL = 'cms:login'
LOGOUT_URL = 'cms:logout'
LOGIN_REDIRECT_URL = '/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '042feo5$3)#*v1em9@-6n751^8cdgw*_o^3evxuo1sayq=n5e_'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
    'boski.context_processors.google_site_verification'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

TEMPLATE_DIRS = (
    'templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.admin',
    # 'django.contrib.admindocs',

    'bootstrap3',
    'taggit',

    'boski',
    'module.web',
    'module.cms',
    'module.about',
    'module.portfolio',
    'module.blog',
    'module.static_page',
)

AUTHENTICATION_BACKENDS = (
    'module.cms.backends.ModelBackendByEmail',
)

try:
    from settings_local import *

    try:
        INSTALLED_APPS += LOCAL_INSTALLED_APPS
    except NameError:
        pass

    try:
        MIDDLEWARE_CLASSES += LOCAL_MIDDLEWARE_CLASSES
    except NameError:
        pass

except ImportError:
    pass
