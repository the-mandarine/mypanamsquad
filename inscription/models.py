# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    FFRS_CHOICES = (('PSquad', 'License FFRS par la Panam Squad'),
                    ('Borrow', 'License FFRS par une autre association'),
                    ('NoSkate', 'License FFRS sans patins'))

    profile_done = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    derby_name = models.CharField(max_length=200)
    derby_number = models.CharField(max_length=5, blank=True)
    real_name = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)
    post_address = models.CharField(max_length=200, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.CharField(max_length=50, blank=True)
    health_certif_date = models.DateField(blank=True, null=True)
    health_certif = models.FileField(blank=True)
    health_problems = models.TextField(blank=True)

    ffrs_status = models.CharField(max_length=8, choices=FFRS_CHOICES, default='PSquad')
    participate_confirmation = models.BooleanField()
    conduct_confirmation = models.BooleanField()
    exact_confirmation = models.BooleanField()
    allow_confirmation = models.BooleanField()

    def __str__(self):
        return "%s (#%s)" % (self.derby_name, self.derby_number)

