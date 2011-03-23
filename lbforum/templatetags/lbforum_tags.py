#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from bbcode import _postmarkup

from djangohelper.decorators import basictag

register = template.Library()

@register.tag
@basictag(takes_context=True)
def bbcode(context, s, has_replied=False):
    if not s:
        return ""
    tag_data = {'has_replied': has_replied}
    html = _postmarkup(s, #cosmetic_replace=False, 
            tag_data=tag_data, 
            auto_urls=getattr(settings, 'BBCODE_AUTO_URLS', True))
    context['hide_attachs'] = tag_data.get('hide_attachs', [])
    return html

@register.simple_tag
def forum_url(forum, topic_type, topic_type2):
    if topic_type and topic_type2:
        return reverse('lbforum_forum_ext2', args=[forum.slug, topic_type, topic_type2])
    if topic_type or topic_type2:
        return reverse('lbforum_forum_ext', args=[forum.slug, topic_type or topic_type2])
    return reverse('lbforum_forum', args=[forum.slug])

@register.simple_tag
def show_attach(attach, post, has_replied, hide_attachs):
    if not has_replied and post.topic_post and \
            (post.topic.need_reply_attachments or hide_attachs.count(u"%s" % attach.pk)):
        return """<a href="#" onclick="alert('%s');return false;">%s</a>""" % \
                (_("reply to see the attachments"), attach.org_filename)
    else:
        return """<a href="%s">%s</a>""" % (attach.file.url, attach.org_filename)

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
