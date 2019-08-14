# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from infos.models import Profile
import date
import unicodedata
import os

class Place(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s (%s)" % (self.name, self.short_name)

class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    desc = models.TextField(default="")
    date = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.PROTECT, null=True, blank=True)
    expected_members = models.ManyToManyField(Profile, blank=True)

    def has_passed:
        return self.date < date.today()

    def __str__(self):
        return "[%s] %s" % (self.date, self.name)

class Attendance(models.Model):
    ATTENDANCE_CHOICES = (('Y', 'Présent'),
                          ('N', 'Absent'),
                          ('P', 'Proxy'))
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attendance = models.CharField(max_length = 1, choices=ATTENDANCE_CHOICES, default = 'N')
    proxy_to = models.ForeignKey(Profile, related_name="proxy_for", on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'member',)

    def __str__(self):
        if self.attendance == 'P':
            return "[%s] %s →  %s" % (self.attendance, self.member.derby_name, self.proxy_to.derby_name)
        else:
            return "[%s] %s" % (self.attendance, self.member.derby_name)

