from django.db import models
from django.contrib.auth.models import User
from infos.models import Profile, ProfileGroup
from datetime import datetime
from pytz import timezone
from django.conf import settings

TZ = timezone(settings.TIME_ZONE)

# Create your models here.
class OpinionQuestion(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=400)
    can_see_answers = models.ManyToManyField(Profile, related_name='can_answer_to', blank=True)
    group_can_see_answers = models.ManyToManyField(ProfileGroup, related_name='can_answer_to', blank=True)
    has_answered = models.ManyToManyField(Profile, related_name='answered_to', blank=True, editable=True)
    def __str__(self):
        return self.name

class Opinion(models.Model):
    question = models.ForeignKey(OpinionQuestion, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()
    def __str__(self):
        return "[%s] %s" % (self.date,  self.text[:150])

