#-*- coding:utf-8 -*-
import urllib
import hashlib
from datetime import datetime, timedelta, date
import os

from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from postmarkup.parser import create, pygments_available, SimpleTag, strip_bbcode as postmarkup_strip_bbcode

from boski.helpers import generate_thumb


register = template.Library()

_postmarkup = create(use_pygments=pygments_available, annotate_links=False)
for i in xrange(1, 7):
    _postmarkup.tag_factory.add_tag(SimpleTag, 'h%d' % i, 'h%d' % i)
render_bbcode = _postmarkup.render_to_html


@register.filter
def rm_kurwa(text):
    """
    Bardzo prosty filter, opierajacy swoje dzialanie na regexpie.
    Dzielimy ciag znakow naczesci po regexpier ktory zawiera przeklenstwa.
    """
    import re

    kurwa_regex = '(?i)chuj|chuje|chuji|chujki|kurwa|kurwy|dziwka|dziwki|dziwko|kutas|kutasy|kutasie|suka|suki|suko|' \
                  'suczko|skurwiel|skurwielu|skurwiele|skurwieli|cwel|cwele|cweli|peneras|chwdp|hwdp'
    return '#$%^&*'.join(re.split(kurwa_regex, text))
rm_kurwa.is_save = True


@register.filter
def bbcode(value):
    """
    Generates (X)HTML from string with BBCode "markup".
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/

    """
    return mark_safe(render_bbcode(value, paragraphs=True))
bbcode.is_save = True


@register.filter
def strip_bbcode(value):
    """
    Strips BBCode tags from a string
    By using the postmark lib from:
    @see: http://code.google.com/p/postmarkup/

    """
    return mark_safe(postmarkup_strip_bbcode(value))
strip_bbcode.is_save = True


@register.filter(name='dir')
def do_dir(value):
    return dir(value)
do_dir.is_save = True


@register.filter
def show_sexy_date(date):
    """
    Wyświetla ładnie sformatowaną datę, w postaci 'wczoraj o 12:34', 'dziś o 8:12'
    :param : datetime
    """
    # jeśli pusty obiekt podajemy, to zwracamy nigdy, w miarę dobre rozwiązanie ;-)
    if date.__class__ == 'NoneType' or date is None or date == '':
        return _('never')

    months = {
        1: 'stycznia', 2: 'lutego', 3: 'marca', 4: 'kwietnia', 5: 'maja', 6: 'czerwca',
        7: 'lipca', 8: 'sierpnia', 9: 'września', 10: 'października', 11: 'listopada', 12: 'grudnia',
    }
    months = {
        1: _('of january'), 2: _('of february'), 3: _('of march'), 4: _('of april'), 5: _('of may'), 6: ('of june'),
        7: _('of july'), 8: _('of august'), 9: _('of september'), 10: _('of october'), 11: _('of november'),
        12: _('of ecember'),
        }
    now = datetime.now()
    if date.tzinfo is not None:
        default_timezone = timezone.get_default_timezone()
        now = timezone.make_aware(now, default_timezone)

    days = now.day - date.day
    minutes = now.minute - date.minute

    delta = now - date  # potrzebne przy pierwszych opcja, gdzie nie minęła godzina, ale będzie różnica przy używaniu days jako wyznacznika

    if delta.seconds.__div__(60) == 0 and delta.days == 0:
        return _('just now')
    elif delta.seconds.__div__(60) == 1 and delta.days == 0:
        return _('minute ago')
    elif delta.seconds.__div__(60) in (2, 3, 4) and delta.days == 0:
        return _('%d minutes ago') % delta.seconds.__div__(60)
    elif 5 < delta.seconds.__div__(60) < 60 and delta.days == 0:  # tutaj cos sie sypalo bez uzyca warunku z delta.days
        return _('%d minutes ago') % delta.seconds.__div__(60)
    elif delta.days < 1 and days == 0:
        return _('today at %d:%02d') % (date.hour, date.minute)
    elif delta.days < 2 and days == 1:
        return _('yesterday at  %d:%02d') % (date.hour, date.minute)
    elif delta.days < 3 and days == 2:
        return _('two days ago at %d:%02d') % (date.hour, date.minute)
    else:
        return _('%d %s %d at %d:%02d') % (date.day, months[date.month], date.year, date.hour, date.minute)


@register.simple_tag
def gravatar(email, size=48):
    """
    Returns url to gravatar icon for given email, with size
    {% gravatar comment.user_email [size] %}
    <img src="{% gravatar mail@company.com 64 %}" />
    """

    url = 'http://www.gravatar.com/avatar.php?%s' % urllib.urlencode({'gravatar_id': hashlib.md5(email).hexdigest(),
                                                                      'size': str(size)})

    return url


@register.simple_tag
def url_namespace(request, name, params_string=''):
    """
        Return URL in current namespace
        {% url gallery:album-overview 'id=123' %}
        {% url_namespace request 'edit' [params] %}
    """

    params = {}

    if params_string:
        params_parts = params_string.split(',')
        count_assignment = params_string.count('=')

        if params_parts.__len__() != count_assignment:
            raise Exception('Only kwargs!')

        for row in params_parts:
            tmp = row.split('=')
            params[tmp[0]] = tmp[1]

    namespace = resolve(request.META['PATH_INFO']).namespace

    url = reverse('%s:%s' % (namespace, name), kwargs=params)

    return url


@register.filter
def prepend_namespace(value, request):
    """ Build
    """
    namespace = resolve(request.META['PATH_INFO']).namespace
    name = '%s:%s' % (namespace, value)

    return name


"""
namefile: usertags.py
You would need a template nest for every method, for example to online_users.
/templates/tag/online_users.html

        {% if user %}
        <ul>
        {% for user in user %}
            <li>{{user.username}}</li>
        {% endfor %}
        </ul>
        {% endif %}

to load

{% load usertags %}
{% online_users 5 %}
{% last_registers 5 %}
{% last_logins 5 %}

"""


@register.inclusion_tag('utils/tags/online_users.html')
def online_users(num):
    """ Show users that were active in last hour. """
    one_hour_ago = datetime.now() - timedelta(hours=1)
    sql_datetime = datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    users = User.objects.filter(last_login__gt=sql_datetime, is_active__exact=1).order_by('-last_login')[:num]
    return {'user': users, }


@register.inclusion_tag('utils/tags/last_registers.html')
def last_registers(num):
    """ Show last registered users """
    users = User.objects.filter(is_active__exact=1).order_by('-date_joined')[:num]
    return {
        'user': users,
    }


@register.inclusion_tag('utils/tags/last_logins.html')
def last_logins(num):
    """ Show last num logged in users (it does shows only that logged in by form) """
    users = User.objects.filter(is_active__exact=1).order_by('-last_login')[:num]
    return {'user': users, }


@register.filter
def get_attr(obj, name):
    """ Try to return attribute by name from obj, otherwise returns None """
    if hasattr(obj, name):
        return getattr(obj, name)

    return None


@register.filter
def get_key(obj, name):
    """ Try to return value by name from obj, otherwise returns None """
    return obj.get(name, None)


@register.simple_tag
def thumbnail(img_url, height=200, width=120, crop=True):
    """
    Generowanie miniaturek relatywnego url
    """
    if not img_url:
        return None

    class img:
        url = img_url
        filename = img_url.split('/')[-1]
        filename_root = ".".join(img_url.split('/')[-1].split('.')[:-1])
        folder = "/".join(img_url.split('/')[:-1]).replace(settings.MEDIA_URL, settings.MEDIA_ROOT + "/")

    thumb_name = "%s_thumb%dx%d.jpg" % (img.filename_root, height, width)

    if not os.path.exists("%s/%s" % (img.folder, thumb_name)):
        try:
            thumb = generate_thumb(open("%s/%s" % (img.folder, img.filename)), (height, width), 'jpg', crop)
        except Exception:
            # import traceback
            # traceback.print_exc()
            return ''

        fh = open("%s/%s" % (img.folder, thumb_name), 'w')
        thumb.seek(0)
        fh.write(thumb.read())
        fh.close()

    return img.url.replace(img.filename, thumb_name)


@register.filter
def fb_thumbnail(img, args=None):
    """
    Generowanie miniaturek z pól FileBrowserField
    """
    if not img:
        return img
    height, width, crop = 200, 120, True
    if args is not None:
        args = [arg.strip() for arg in args.split(',')]
        height = int(args[0])
        width = int(args[1])
        if args.__len__() == 3 and args[2] == '0':
            crop = False

    thumb_name = "%s_thumb%dx%d.jpg" % (img.filename_root, height, width)

    if not os.path.exists("%s/%s" % (img.path.replace(img.filename, ''), thumb_name)):
        try:
            thumb = generate_thumb(open(img.path), (height, width), 'jpg', crop)
        except IOError: # brak pliku
            return ''
        except Exception: # lol
            return ''
        fh = open("%s/%s" % (img.path.replace(img.filename, ''), thumb_name), 'w')
        thumb.seek(0)
        fh.write(thumb.read())
        fh.close()

    return img.url.replace(img.filename, thumb_name)


def create_dir_hash_structure(hash_name, under_path, blocs=4):
    created_part = ''

    for i in xrange(0, blocs):
        created_part = os.path.join(created_part, hash_name[i * 2:(i + 1) * 2])

        try:
            os.mkdir(os.path.join(under_path, created_part))
        except Exception, e:
            if e.errno == 17:  # file (dir in this case) exist error
                pass
            else:  # re-raise
                raise

    return os.path.join(under_path, created_part), created_part


@register.filter
def thumbnail2(img_url, args=None):
    """
    Generowanie miniaturek relatywnego url
    """
    if not img_url:
        return img_url

    class img:
        url = img_url
        filename = img_url.split('/')[-1]
        filename_root = ".".join(img_url.split('/')[-1].split('.')[:-1])
        folder = "/".join(img_url.split('/')[:-1]).replace(settings.MEDIA_URL, settings.MEDIA_ROOT + "/")

    height, width, crop = 200, 120, True
    if args is not None:
        args = [arg.strip() for arg in args.split(',')]
        height = int(args[0])
        width = int(args[1])
        if args.__len__() == 3 and args[2] == '0':
            crop = False

    thumb_name = "%s_thumb%dx%d.jpg" % (img.filename_root, height, width)

    if not os.path.exists("%s/%s" % (img.folder, thumb_name)):
        try:
            thumb = generate_thumb(open("%s/%s" % (img.folder, img.filename)), (height, width), 'jpg', crop)
        except Exception:
            # import traceback
            # traceback.print_exc()
            return ''

        fh = open("%s/%s" % (img.folder, thumb_name), 'w')
        thumb.seek(0)
        fh.write(thumb.read())
        fh.close()

    return img.url.replace(img.filename, thumb_name)


@register.simple_tag()
def thumbnail_c(img_url, height=200, width=120, crop=True):
    """
    @param img_url: ImageFieldFile
    Generowanie miniaturek relatywnego url
    """
    if not img_url:
        return img_url

    if img_url.__class__.__name__ == 'ImageFieldFile':
        img_url = img_url.name

    img_url = urllib.unquote(img_url)
    filename = img_url.split('/')[-1]  # nazwa pliku
    filename_root = ".".join(img_url.split('/')[-1].split('.')[:-1])  # ścieżka do pliku
    folder = "/".join(img_url.split('/')[:-1]).replace(settings.MEDIA_URL,
                                                       settings.MEDIA_ROOT + "/")  # ścieżka do miniaturki

    if not folder.startswith(settings.MEDIA_ROOT):
        folder = '%s/%s' % (settings.MEDIA_ROOT, folder)

    thumb_name = "%s.jpg" % hashlib.sha256("%s_thumb%dx%d.jpg" % (filename_root, height, width)).hexdigest()

    created_path, hash_part = create_dir_hash_structure(thumb_name, settings.MEDIA_ROOT + '/photo', 7)

    full_thumbnail_path = "%s/%s" % (created_path, thumb_name.replace(''.join(hash_part.split('/')), ''))
    full_thumbnail_url = "photo/%s/%s" % (hash_part, thumb_name.replace(''.join(hash_part.split('/')), ''))

    if not os.path.exists(full_thumbnail_path):
        try:
            with open("%s/%s" % (folder, filename)) as fh:
                thumb = generate_thumb(fh, (height, width), 'jpg', crop)
        except IOError, e:
            return None

        if thumb is None:
            return None

        with open(full_thumbnail_path, 'w') as fh:
            thumb.seek(0)
            fh.write(thumb.read())

    return full_thumbnail_url


@register.filter
def match_url(url, match_with):
    return url.startswith(match_with)


@register.filter
def exact_match_url(url, match_with):
    return url == match_with


@register.simple_tag(takes_context=True)
def try_to_include(context, template_name):
    """
    Try to include a template, if doesn't exists, return empty string.
    Usage: {% try_to_include "head.html" %}
    """

    try:
        return template.loader.get_template(template_name).render(context)
    except template.TemplateDoesNotExist:
        return ''


@register.filter
def get_default_path(value, request):
    namespace = resolve(request.META['PATH_INFO']).namespace
    if ':' in namespace:
        namespace = '/'.join(namespace.split(':'))

    path = '%s/%s' % (namespace, value)

    return path


@register.filter
def within_time(datetime_obj, value):
    """
    Checks if datetime_obj is within given period
    Suffixes:
    d - days
    h - hours
    m - minutes
    s - secounds
    @param datetime_obj: datetime or date
    @param value: string - must match (\d+)(d|h|m|s)
    @return:
    """
    value, suffix = int(value[:-1]), value[-1]

    if isinstance(datetime_obj, date):
        datetime_obj = datetime.combine(datetime_obj, datetime.min.time())
    elif not isinstance(datetime_obj, datetime):  # not a datetime or date object
        raise Exception(_('Instance of `date` or `datetime` expected.'))

    if suffix == 'd':
        return datetime.now() < datetime_obj + timedelta(days=value)
    elif suffix == 'h':
        return datetime.now() < datetime_obj + timedelta(hours=value)
    elif suffix == 'm':
        return datetime.now() < datetime_obj + timedelta(minutes=value)
    elif suffix == 's':
        return datetime.now() < datetime_obj + timedelta(seconds=value)
    else:
        raise Exception(_('Incorrect suffix supplied'))


