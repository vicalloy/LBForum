# -*- coding: UTF-8 -*-
import datetime

from django import template
from django.template.defaultfilters import timesince as _timesince
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.conf import settings
from dateutil import tz

from .bbcode import _postmarkup

register = template.Library()


@register.filter
def bbcode(s):
    if not s:
        return ""
    html = _postmarkup(
        s,  # cosmetic_replace=False,
        auto_urls=getattr(settings, 'BBCODE_AUTO_URLS', True))
    return mark_safe(html)


@register.filter
def form_all_error(form):
    errors = []
    global_error = form.errors.get('__all__', '')
    if global_error:
        global_error = global_error.as_text()
    for name, field in form.fields.items():
        e = form.errors.get(name, '')
        if e:
            errors.append((field.label, force_text(e), ))
    return mark_safe(
        u'<ul class="errorlist">%s %s</ul>' % (
            global_error, ''.join([u'<li>%s%s</li>' % (k, v) for k, v in errors])))


@register.filter
def topic_state(topic):
    c = []
    if topic.closed:
        c.append('closed')
    elif topic.sticky:
        c.append('sticky')
    else:
        c.append('normal')
    return ' '.join(c)


@register.filter
def post_style(forloop):
    styles = ''
    if forloop['first']:
        styles = 'firstpost topicpost'
    else:
        styles = 'replypost'
    if forloop['last']:
        styles += ' lastpost'
    return styles


@register.filter
def online(user):
    try:
        if user.online.online():
            return _('Online')
    except:
        pass
    return _('Offline')


@register.filter
def lbtimesince(d, now=None):
    # Convert datetime.date to datetime.datetime for comparison.
    from_zone = tz.gettz('UTC')
    if not d:
        return ''
    # '2016-07-05T08:08:21.421Z'
    if isinstance(d, (str, six.text_type)):
        tmp_d = None
        try:
            tmp_d = datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            pass
        try:
            tmp_d = datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
        except:
            pass
        if tmp_d:
            d = tmp_d.replace(tzinfo=from_zone)
        else:
            return ''
    if not now:
        now = timezone.now()
    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since // (60 * 60 * 24) < 3:
        return _("%s ago") % _timesince(d)
    # return _date(d, "Y-m-d H:i")
    return d


@register.filter
def post_count(user):
    return user.post_set.filter(topic_post=False).count()


@register.filter
def topic_can_post(topic, user):
    if not topic:
        return False
    forum = topic.forum
    return forum.is_admin(user) or not topic.closed
