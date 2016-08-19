# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import re

from django import template
from django.utils.translation import ugettext
from django.conf import settings
from django.core.urlresolvers import reverse

from postmarkup import create, QuoteTag, TagBase, PostMarkup, strip_bbcode

from lbattachment.models import LBAttachment

from .helper import clean_html

register = template.Library()

# bbcode
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
            return '<div class="quotebox"><cite>%s:</cite><blockquote><p>' % (PostMarkup.standard_replace(self.params))
        else:
            return '<div class="quotebox"><blockquote><p>'

    def render_close(self, parser, node_index):
        return "</p></blockquote></div>"


class VideoTag(TagBase):

    def __init__(self, name, **kwargs):
        TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        video_url = self.get_contents_text(parser)
        self.skip_contents(parser)
        html = """
  <video controls="controls" preload="none">
    <source type="video/mp4" src="%s" />
    <object type="application/x-shockwave-flash" data="flashmediaelement.swf">
      <param name="movie" value="%smediaelement/build/flashmediaelement.swf" />
      <param name="flashvars" value="controls=true&amp;file=%s" />
    </object>
  </video>
        """ % (video_url, settings.STATIC_URL, video_url)
        return html


class AttachTag(TagBase):

    def __init__(self, name, **kwargs):
        TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        self.skip_contents(parser)
        try:
            attach = LBAttachment.objects.get(pk=contents)
        except:
            return '[attach]%s[/attach]' % contents
        url = "%s?pk=%s" % (reverse('lbattachment_download'), attach.pk)
        return '<a title="%s" href="%s">%s</a>' % (
            attach.description,
            url, attach.filename)


class AttachImgTag(TagBase):

    def __init__(self, name, **kwargs):
        TagBase.__init__(self, name, inline=True)

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        self.skip_contents(parser)
        try:
            attach = LBAttachment.objects.get(pk=contents)
        except:
            return u'[attachimg]%s[/attachimg]' % contents
        url = "%s?pk=%s" % (reverse('lbattachment_download'), attach.pk)
        return u'<img title="%s" src="%s"/>' % (
            attach.description,
            url)


class HTMLTag(TagBase):

    def render_open(self, parser, node_index):
        contents = self.get_contents(parser)
        contents = strip_bbcode(contents)
        self.skip_contents(parser)
        return clean_html(contents)

pygments_available = True
try:
    from pygments import highlight  # NOQA
    from pygments.lexers import get_lexer_by_name, ClassNotFound  # NOQA
    from pygments.formatters import HtmlFormatter  # NOQA
except ImportError:
    # Make Pygments optional
    pygments_available = False

_postmarkup = create(use_pygments=pygments_available, annotate_links=False)
_postmarkup.tag_factory.add_tag(LBQuoteTag, 'quote')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'replyview')
_postmarkup.tag_factory.add_tag(ReplyViewTag, 'hide')
_postmarkup.tag_factory.add_tag(AttachTag, 'attach')
_postmarkup.tag_factory.add_tag(AttachImgTag, 'attachimg')
_postmarkup.tag_factory.add_tag(HTMLTag, 'html')
_postmarkup.tag_factory.add_tag(VideoTag, 'video')
