#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from simplejson import dumps
from django.utils.translation import ugettext_lazy as _


class ActionLog(models.Model):
    """
    action_type - na razie plain text, z czasem wyjdzie jakie są potrzebna pola, obecnie:
        - login
        - login_attempt
        - create
        - update
        - delete
        - mark_delete
        - mark
    """
    user = models.ForeignKey(User, null=True, blank=True) #, related_name='login_log')
    # username = models.CharField('Nazwa użytkownika', max_length=255, null=True, blank=True)
    # password = models.BooleanField('Czy używał hasła')
    created_at = models.DateTimeField('Data logowania', default=datetime.now())
    ip = models.IPAddressField('IP')
    ua = models.CharField('User agent', max_length=255)
    # success = models.BooleanField('Czy logowanie udane')
    post_data = models.TextField('Dane wysłane POSTem')
    get_data = models.TextField('Dane wysłane GETem')
    session_data = models.TextField('Dane zapisane w sesji')
    meta_data = models.TextField('Dane zapisane w request.META')
    cookies_data = models.TextField('Dane zapisane w ciastkach')

    action_type = models.CharField('Typa akcji', max_length=96)
    message = models.TextField('Wiadomość dla akcji')

    LOGIN = 'login'
    LOGOUT = 'logout'
    LOGIN_ATTEMPT = 'login_attempt'
    PASSWORD_CHANGE = 'password_change'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    MARK_DELETE = 'mark_delete'
    MARK = 'mark'
    ERROR = 'error'
    DEBUG = 'debug'
    EXCEPTION = 'exception'
    INFO = 'info'

    class Meta:
        verbose_name = 'Logowanie'
        verbose_name_plural = 'Logowania'

    def __unicode__(self):
        return u'Wpis z dnia %s' % self.created_at

    @staticmethod
    def log(request, action_type=None, message=None):
        """ Static method to easily log informations """
        meta_dict = {}
        for k in request.META:
            try:
                meta_dict[k] = '%s' % request.META[k]
            except TypeError:
                meta_dict[k] = request.META[k].__str__()

        entry = ActionLog()
        entry.ua = request.META['HTTP_USER_AGENT']
        entry.ip = request.META['REMOTE_ADDR']
        entry.post_data = dumps(request.POST)
        entry.get_data = dumps(request.GET)
        entry.session_data = request.session.load()
        entry.cookies_data = dumps(request.COOKIES)
        entry.meta_data = dumps(meta_dict)
        entry.action_type = action_type
        entry.message = message

        if isinstance(request.user, User):
            entry.user = request.user

        entry.save()

    @staticmethod
    def mark(request):
        """ Simply mark """
        ActionLog.log(request, ActionLog.MARK, 'MARK')

