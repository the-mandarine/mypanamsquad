# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    FFRS_CHOICES = (('PSquad', 'License FFRS par la Panam Squad'),
                    ('Borrow', 'License FFRS par une autre association'),
                    ('NoSkate', 'License FFRS sans patins'))

    # bypass for votes
    has_been_checked = models.BooleanField(default = False)
    # validation from secretary and treasurer
    has_paid_dues = models.BooleanField(default = False)
    has_filled_profile = models.BooleanField(default = False)

    # actual profile
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

    ffrs_status = models.CharField(max_length=8, choices=FFRS_CHOICES, default='PSquad')

    def is_full_member(self):
        return self.has_paid_dues and self.has_filled_profile
    is_full_member.boolean = True

    def __str__(self):
        return "%s (#%s)" % (self.derby_name, self.derby_number)

class ProfileGroup(models.Model):
    name = models.CharField(max_length=200)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return "%s (%s)" % (self.name, self.profiles.count())
