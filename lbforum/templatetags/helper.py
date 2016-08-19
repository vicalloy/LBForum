# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup, NavigableString

acceptable_elements = [
    'a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
    'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
    'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
    'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
    'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
    'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
    'thead', 'tr', 'tt', 'u', 'ul', 'var']

acceptable_attributes = [
    'abbr', 'accept', 'accept-charset', 'accesskey',
    'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
    'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
    'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
    'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
    'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
    'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
    'usemap', 'valign', 'value', 'vspace', 'width', 'style']

acceptable_elements.extend(getattr(settings, 'HTML_SAFE_TAGS', []))
acceptable_attributes.extend(getattr(settings, 'HTML_SAFE_ATTRS', []))
acceptable_elements = set(acceptable_elements) - set(getattr(settings, 'HTML_UNSAFE_TAGS', []))
acceptable_attributes = set(acceptable_attributes) - set(getattr(settings, 'HTML_UNSAFE_ATTRS', []))


def clean_html(fragment):
    soup = BeautifulSoup(fragment.strip())

    def cleanup(soup):
        for tag in soup:
            if not isinstance(tag, NavigableString):
                if tag.name not in acceptable_elements:
                    tag.extract()
                else:
                    keys_to_del = []
                    for attr in tag.attrs.keys():
                        if attr not in acceptable_attributes:
                            keys_to_del.append(attr)
                    for key in keys_to_del:
                        del tag[key]
                    cleanup(tag)
    cleanup(soup)
    return mark_safe(soup)
