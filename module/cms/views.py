# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, authenticate, login as auth_login
from django.core.urlresolvers import reverse
from django.contrib import messages
from boski.helpers.others import get_values

from boski.mixins import LoginRequiredMixin, BreadcrumbsMixin
from boski.views.crud import ListView
from module.cms.forms import PasswordChangeForm, LoginForm
from module.cms.models import ActionLog
from boski.decorators import with_template


class IndexView(LoginRequiredMixin, BreadcrumbsMixin, TemplateView):
    template_name = 'cms/index.html'


class Login(FormView):
    form_class = LoginForm
    template_name = 'cms/login.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email', None)
        password = form.cleaned_data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(self.request, user)
                messages.success(self.request, _('You have been successfully logged in'))
                ActionLog.log(self.request, ActionLog.LOGIN, _('Login successful'))

                return super(Login, self).form_valid(form)
            else:
                messages.error(self.request, _('Your account is inactive'))
                ActionLog.log(self.request, ActionLog.LOGIN_ATTEMPT, _('Login on inactive account'))
        else:
            messages.error(self.request, _('Wrong login credentials'))
            ActionLog.log(self.request, ActionLog.LOGIN_ATTEMPT, _('Wrong login credentials'))

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.request.GET.get('next', reverse('cms:index'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Login, self).get(request, *args, **kwargs)


class Logout(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        ActionLog.log(self.request, ActionLog.LOGOUT, _('Logout'))
        return auth_views.logout(self.request, next_page=reverse('cms:index'))


@login_required
@with_template('cms/change_password.html')
def change_password(request):
    """ Change password view """
    back = request.GET.get('back', None)
    if back is None:
        back = reverse('cms:index')

    form = PasswordChangeForm(request.user, request.POST or None)

    if form.is_valid():
        try:
            request.user.set_password(form.cleaned_data['new_password1'])
            messages.success(request, _('Your password has been changed'))
            ActionLog.log(request, ActionLog.PASSWORD_CHANGE, _('Password change'))
            return HttpResponseRedirect(back)
        except:
            ActionLog.log(request, ActionLog.EXCEPTION, _('Error occurred during changing password'))
            messages.error(request, _('An error has occurred during changing password'))

    name = _('Password change')
    request.breadcrumbs = ({'name': name, 'url': 'cms:change-password'},)

    return locals()


class Log(ListView, LoginRequiredMixin):
    queryset = ActionLog.objects.all()

    breadcrumbs = ({'name': _('Action log'), 'url': 'cms:log'},)

    listingColumns = (
        ('id', '#'),
        ('user', _('User')),
        ('action_type', _('Type')),
        ('message', _('Message')),
        ('created_at', _('Created at'))
    )

    action_type_options = {
        ActionLog.LOGIN: _('Login'),
        ActionLog.LOGIN_ATTEMPT: _('Login attempt'),
        ActionLog.LOGOUT: _('Logout'),
        ActionLog.PASSWORD_CHANGE: _('Password change'),
        ActionLog.CREATE: _('Create entry'),
        ActionLog.UPDATE: _('Update entry'),
        ActionLog.DELETE: _('Delete entry'),
        ActionLog.MARK_DELETE: _('Entry marked as deleted'),
        ActionLog.MARK: _('Mark'),
        ActionLog.ERROR: _('Error'),
        ActionLog.EXCEPTION: _('Exception'),
        ActionLog.DEBUG: _('Debug'),
        ActionLog.INFO: _('Information'),
    }

    filters = (
        ('action_type__exact', {
            'label': _('Type'),
            'type': 'select',
            'class': 'none',
            'options': dict({'': '---'}.items() + action_type_options.items())
        }),
        ('created_at__gte', {'label': _('Created from'), 'type': 'text', 'class': 'calendar'}),
        ('created_at__lte', {'label': _('To'), 'type': 'text', 'class': 'calendar'})
    )

    mapColumns = {
        'id': '_displayAsIs',
        'user': '_displayAsIs',
        'action_type': '_displayAsIs',
        'message': '_displayAsIs',
        'created_at': '_displayDateTime'
    }

    orderingColumns = {'id', 'user', 'action_type', 'message', 'created_at'}
    searchColumns = ['id', 'user', 'action_type', 'message']
    actions = {'index': 'log', }
    allow_create = False
    allow_update = False
    allow_delete = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            self.queryset = self.queryset.filter(user=request.user)

        return super(Log, self).dispatch(request, *args, **kwargs)

    def prepare_response_data(self, data):
        response_data = super(Log, self).prepare_response_data(data)

        user_list = get_values(User.objects.all(), ('username', 'first_name', 'last_name', 'email'), 'pk')

        for i in response_data:
            if response_data[i]['user']:
                pk = response_data[i]['user']
                response_data[i]['user'] = user_list[pk]['first_name'] + ' ' + user_list[pk]['last_name'] \
                    if user_list[pk]['first_name'] or user_list[pk]['last_name'] else user_list[pk]['username']
            else:
                response_data[i]['user'] = '---'

            response_data[i]['action_type'] = self.action_type_options[response_data[i]['action_type']] \
                if response_data[i]['action_type'] else '---'

        return response_data
