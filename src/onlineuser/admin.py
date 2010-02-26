#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Online

class OnlineAdmin(admin.ModelAdmin):
    list_display        = ('user', 'ident', 'updated_on', 'created_on',)
    search_fields       = ('ident', )

admin.site.register(Online, OnlineAdmin)
