#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import template

register = template.Library()

@register.simple_tag
def getvars(request, excludes):
    getvars = request.GET.copy()
    excludes = excludes.split(',')
    for p in excludes:
        if p in getvars:
            del getvars[p]
        if len(getvars.keys()) > 0:
            return "&%s" % getvars.urlencode()
        else:
            return ''
