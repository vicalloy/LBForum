#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime

from django import template
from django.template.defaultfilters import timesince as _timesince
from django.template.defaultfilters import date as _date
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.tzinfo import LocalTimezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from bbcode import _postmarkup

register = template.Library()

@register.filter
def bbcode(s):
    if not s:
        return ""
    return _postmarkup(s, cosmetic_replace=False, 
            auto_urls=getattr(settings, 'BBCODE_AUTO_URLS', True))

@register.filter
def form_all_error(form):
    errors = []
    global_error = form.errors.get('__all__', '')
    if global_error:
        global_error = global_error.as_text()
    for name, field in form.fields.items():
        e = form.errors.get(name, '')
        if e:
            errors.append((field.label, force_unicode(e), ))
    return mark_safe(u'<ul class="errorlist">%s %s</ul>'
            % (global_error, ''.join([u'<li>%s%s</li>' % (k, v) for k, v in errors])))

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
    if not d:
        return ''
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)
    if not now:
        if d.tzinfo:
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now()
    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since // (60 * 60 * 24) < 3:
        return _("%s ago") % _timesince(d)
    return _date(d, "Y-m-d H:i")

@register.simple_tag
def page_item_idx(page_obj, forloop):
    return page_obj.start_index() + forloop['counter0']

@register.simple_tag
def page_range_info(page_obj):
    paginator = page_obj.paginator
    if paginator.num_pages == 1:
        return paginator.count
    return str(page_obj.start_index()) +' ' + 'to' + ' ' +  \
            str(page_obj.end_index()) + ' ' + 'of' + ' ' +  str(page_obj.paginator.count)

DEFAULT_PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 20)
DEFAULT_WINDOW = getattr(settings, 'PAGINATION_DEFAULT_WINDOW', 4)

@register.inclusion_tag('lbforum/post_paginate.html', takes_context=True)
def post_paginate(context, count, paginate_by=DEFAULT_PAGINATION, window=DEFAULT_WINDOW):
    if not isinstance(paginate_by, int):
        paginate_by = template.Variable(paginate_by)
    if not isinstance(window, int):
        window = template.Variable(paginate_by)
    page_count = count / paginate_by
    if count % paginate_by > 0:
        page_count += 1
    context['page_count'] = page_count
    pages = []
    if page_count == 1:
        pass
    elif window >= page_count:
        pages = [e + 1 for e in range(page_count)]
    else:
        pages = [e + 1 for e in range(window-1)]
    context['pages'] = pages
    context['window'] = window
    return context
