#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re

from django import template
from django.utils.translation import ugettext

from postmarkup import create, QuoteTag, TagBase, PostMarkup, strip_bbcode

from attachments.models import Attachment

from helper import clean_html

register = template.Library()

#bbcode
_RE_ATTACH = r"""\[attach\](\d*?)\[/attach\]"""
_RE_ATTACHIMG = r"""\[attachimg\](\d*?)\[/attachimg\]"""

class ReplyViewTag(TagBase):

    def render_open(self, parser, node_index):
        tag_data = parser.tag_data
        if not tag_data.get('has_replied', False):
            self.skip_contents(parser)
            contents = self.get_contents(parser)
            hide_attach = tag_data.get('hide_attachs', [])
            hide_attach.extend(re.findall(_RE_ATTACH, contents))
            hide_attach.extend(re.findall(_RE_ATTACHIMG, contents))
            tag_data['hide_attachs'] = hide_attach
            return '<p class="need-reply">%s</p>' % ugettext("to see the content, user must reply first.")
        return ""

class LBQuoteTag(QuoteTag):

    def render_open(self, parser, node_index):
        if self.params:
            return u'<div class="quotebox"><cite>%s:</cite><blockquote><p>'%(PostMarkup.standard_replace(self.params))
        else:
            return u'<div class="quotebox"><blockquote><p>'


    def render_close(self, parser, node_index):
        return u"</p></blockquote></div>"

class AttachTag(TagBase):

    def __init__(self, name, **kwargs):
        TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        self.skip_contents(parser)
        try:
            attach = Attachment.objects.get(pk=contents)
        except:
            return u'[attach]%s[/attach]' % contents
            pass
        return u'<a title="%s" href="%s">%s</a>' % (attach.description, \
                attach.file.url, attach.org_filename)

class AttachImgTag(TagBase):

    def __init__(self, name, **kwargs):
        TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        self.skip_contents(parser)
        try:
            attach = Attachment.objects.get(pk=contents)
        except:
            return u'[attachimg]%s[/attachimg]' % contents
            pass
        return u'<img title="%s" src="%s"/>' % (attach.description, \
                attach.file.url)

class HTMLTag(TagBase):

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        contents = strip_bbcode(contents)
        self.skip_contents(parser)
        return clean_html(contents)


_postmarkup = create(use_pygments=False, annotate_links=False)
_postmarkup.tag_factory.add_tag(LBQuoteTag, 'quote')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'replyview')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'hide')
_postmarkup.tag_factory.add_tag(AttachTag, 'attach')
_postmarkup.tag_factory.add_tag(AttachImgTag, 'attachimg')
_postmarkup.tag_factory.add_tag(HTMLTag, 'html')
