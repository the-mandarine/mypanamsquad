# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from infos.models import Profile
import unicodedata
import os


# Create your models here.
class Player(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='uploads/photos', blank=True)

    def __str__(self):
        return "#%s %s" % (self.profile.derby_number, self.profile.derby_name)

class TrainingPart(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default="part")
    desc = models.TextField(blank=True)
    people = models.ManyToManyField(Player)

class Training(models.Model):
    date = models.DateField()
    parts = models.ManyToManyField(TrainingPart)

    def __str__(self):
        return "%s" % (self.date)
