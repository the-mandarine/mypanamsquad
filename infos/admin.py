# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from infos.models import Profile, ProfileGroup

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'has_been_checked']}),
        ('Administrative', {'fields': [
            'has_paid_dues',
            'has_filled_profile',
        ]}),
        ('Derby status', {'fields': [
            'derby_name',
            'derby_number',
        ]}),
        ('Personal informations', {'fields': [
                'real_name',
                'birth_date',
                'contact_email',
                'contact_phone',
                'post_address',
                'postal_code',
                'city',
        ]}),
    ]
#    filter_horizontal = ('derby_roles',)
    list_display = ('derby_name', 'derby_number', 'has_been_checked', 'is_full_member',)

class ProfileGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('profiles',)
    list_display = ('name', 'user_count',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileGroup, ProfileGroupAdmin)

