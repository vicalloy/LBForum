# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .bbcode import _postmarkup

register = template.Library()


@register.simple_tag(takes_context=True)
def bbcode(context, s, has_replied=False):
    if not s:
        return ""
    tag_data = {'has_replied': has_replied}
    html = _postmarkup(
        s,  # cosmetic_replace=False,
        tag_data=tag_data,
        auto_urls=getattr(settings, 'BBCODE_AUTO_URLS', True))
    context['hide_attachs'] = tag_data.get('hide_attachs', [])
    return mark_safe(html)


@register.simple_tag
def forum_url(forum, topic_type, topic_type2):
    args = [forum.slug, topic_type, topic_type2]
    args = [e for e in args if e]
    return reverse('lbforum_forum', args=args)


@register.simple_tag
def show_attach(attach, post, has_replied, hide_attachs):
    if not has_replied and post.topic_post and \
            (post.topic.need_reply_attachments or hide_attachs.count(u"%s" % attach.pk)):
        html = """<a href="#" onclick="alert('%s');return false;">%s</a>""" % \
            (_("reply to see the attachments"), attach.filename)
    else:
        url = "%s?pk=%s" % (reverse('lbattachment_download'), attach.pk)
        html = """<a href="%s">%s</a>""" % (url, attach.filename)
    return mark_safe(html)


@register.simple_tag
def page_item_idx(pages, forloop):
    return pages.current_start_index() + forloop['counter0']


@register.simple_tag
def page_range_info(pages):
    if pages.paginated:
        return pages.total_count()
    return "%s to %s of %s" % (
        pages.current_start_index(), pages.current_end_index(),
        pages.total_count())

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
        pages = [e + 1 for e in range(window - 1)]
    context['pages'] = pages
    context['window'] = window
    return context
