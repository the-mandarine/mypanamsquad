# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Password(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return "%s (%s)" % (self.name, self.url)
