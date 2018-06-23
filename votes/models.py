from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Vote(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=400)
    can_vote = models.ManyToManyField(User, related_name='can_vote_for', blank=True)
    has_voted = models.ManyToManyField(User, related_name='voted_for', blank=True)
    pub_date = models.DateTimeField('date published', blank=True, default=datetime.now)
    end_date = models.DateTimeField('end date', blank=True, default=datetime.now)
    def __str__(self):
        return self.name

class VoteItem(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    results = models.IntegerField(default=0)
    def __str__(self):
        return "[%s] %s" % (self.vote.name, self.text)

