#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Avatar

class AvatarAdmin(admin.ModelAdmin):
    list_display        = ('user', 'avatar', 'date_uploaded',)
    search_fields       = ('user', )

admin.site.register(Avatar, AvatarAdmin)
