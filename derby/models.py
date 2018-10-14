# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from infos.models import Profile
import unicodedata
import os


# Create your models here.
class Player(models.Model):
    PHOTO_DIR = 'uploads/photos'
    DEFAULT_PHOTO = 'static/imgs/player_default.png'
    DEFAULT_PHOTO2 = 'static/imgs/player_default.png'
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    photo = models.FileField(upload_to=PHOTO_DIR, blank=True)
    photo2 = models.FileField(upload_to=PHOTO_DIR, blank=True)

    def __str__(self):
        return "#%s %s" % (self.profile.derby_number, self.profile.derby_name)

class Place(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s (%s)" % (self.name, self.short_name)

class TrainingPartType(models.Model):
    BUTTON_CHOICES = (('default', 'Gris'),
                      ('primary', 'Bleu'),
                      ('success', 'Vert'),
                      ('info', 'Cyan'),
                      ('warning', 'Orange'),
                      ('danger', 'Rouge'),
                      ('inverse', 'Noir'),
                      ('link', 'Sans couleur'),
                     )
    name = models.CharField(max_length=100)
    button_color = models.CharField(max_length=8, choices=BUTTON_CHOICES)
    def __str__(self):
        return "%s" % (self.name)

class Training(models.Model):
    date = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.date, str(self.place))

class TrainingPart(models.Model):
    name = models.CharField(max_length=200)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='parts', null=True)
    kind = models.ForeignKey(TrainingPartType, on_delete=models.PROTECT, null=True, default=None)
    desc = models.TextField(blank=True)
    people = models.ManyToManyField(Player, blank=True, editable=False)
    def __str__(self):
        if self.training and self.training.place:
            return "%s - %s (%s)" % (self.training.date, self.name, self.training.place.short_name)
        elif self.training:
            return "%s - %s (-)" % (self.training.date, self.name)
        return "(orphan) - %s (-)" % (self.name)

