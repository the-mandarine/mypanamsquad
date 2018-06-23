from django.contrib import admin

# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from votes.models import Vote, VoteItem

class VoteAdmin(admin.ModelAdmin):
    filter_horizontal = ('can_vote', 'has_voted')

admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteItem)
