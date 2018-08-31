# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from infos.models import Profile, ProfileGroup, Member

class ProfileAdmin(admin.ModelAdmin):
#    filter_horizontal = ('derby_roles',)
    list_display = ('derby_name', 'derby_number', 'has_been_checked',)

class ProfileGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('profiles',)
    list_display = ('name', 'user_count',)

class MemberAdmin(admin.ModelAdmin):
#    filter_horizontal = ('derby_roles',)
    list_display = ('display_name', 'submitted', 'has_paid', 'validated',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileGroup, ProfileGroupAdmin)

admin.site.register(Member, MemberAdmin)

