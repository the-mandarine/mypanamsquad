from django.contrib import admin

# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from votes.models import Vote, VoteItem

class VoteItemInline(admin.TabularInline):
    model = VoteItem
    extra = 1

class VoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'text']}),
        ('Members', {'fields': ['can_vote', 'has_voted']}),
        ('Dates', {'fields': ['pub_date', 'end_date']}),
    ]
    filter_horizontal = ('can_vote', 'has_voted')
    inlines = [VoteItemInline]
    list_display = ('name', 'pub_date', 'end_date', 'get_vote_status',)
    list_filter = ['pub_date']

admin.site.register(Vote, VoteAdmin)
