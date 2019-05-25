from django.contrib import admin

# Register your models here.
from django.db import models
from opinions.models import OpinionQuestion

class OpinionQuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('can_see_answers', 'group_can_see_answers', )

admin.site.register(OpinionQuestion, OpinionQuestionAdmin)
