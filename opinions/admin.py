from django.contrib import admin

# Register your models here.
from django.db import models
from opinions.models import OpinionQuestion, OpinionSubQuestion

class OpinionSubQuestionInline(admin.TabularInline):
    model = OpinionSubQuestion
    extra = 1

class OpinionQuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('can_answer', 'can_see_answers', 'group_can_see_answers', )
    inlines = [OpinionSubQuestionInline]

admin.site.register(OpinionQuestion, OpinionQuestionAdmin)
