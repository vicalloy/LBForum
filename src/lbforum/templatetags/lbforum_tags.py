#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings

from bbcode import _postmarkup

register = template.Library()

@register.simple_tag
def bbcode(s, has_replied=False):
    if not s:
        return ""
    tag_data = {'has_replied': has_replied}
    return _postmarkup(s, cosmetic_replace=False, tag_data=tag_data)
#bbcode end

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
