#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import template
from django.utils.translation import ugettext

from postmarkup import create, QuoteTag, TagBase, PostMarkup
from helper import clean_html

register = template.Library()

#bbcode
class ReplyViewTag(TagBase):

    def render_open(self, parser, node_index):
        tag_data = parser.tag_data
        if not tag_data.get('has_replied', False):
            self.skip_contents(parser)
            return '<p class="need-reply">%s</p>' % ugettext("to see the content, user must reply first.")
        return ""

    def render_close(self, parser, node_index):
        return ""

class LBQuoteTag(QuoteTag):

    def render_open(self, parser, node_index):
        if self.params:
            return u'<div class="quotebox"><cite>%s:</cite><blockquote><p>'%(PostMarkup.standard_replace(self.params))
        else:
            return u'<div class="quotebox"><blockquote><p>'


    def render_close(self, parser, node_index):
        return u"</p></blockquote></div>"

class HTMLTag(TagBase):

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        self.skip_contents(parser)
        return clean_html(contents)


_postmarkup = create(use_pygments=False, annotate_links=False)
_postmarkup.tag_factory.add_tag(LBQuoteTag, 'quote')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'replyview')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'hide')
_postmarkup.tag_factory.add_tag(HTMLTag, 'html')
