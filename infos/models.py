# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):

    # bypass for votes
    has_been_checked = models.BooleanField(default = False)

    # actual profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    derby_name = models.CharField(max_length=200)
    derby_number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return "%s (#%s)" % (self.derby_name, self.derby_number)

class Member(models.Model):
    FFRS_CHOICES = (('PComp', 'License FFRS Panam Squad "compétition"'),
                    ('PLois', 'License FFRS Panam Squad "loisir"'),
                    ('PFoot', 'License FFRS Panam Squad "non-pratiquant"'),
                    ('OBorr', 'License FFRS par une autre association'),
                    ('NoLic', 'Pas de license FFRS'))

    ROLE_CHOICES = (('P', 'Jouer'),
                    ('O', 'Officier/Arbitrer'),
                    ('C', 'Coacher'),
                    ('V', 'Donner un coup de main/Speaker'))

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=200)
    has_been_processed = models.BooleanField(default = False)
    birth_date = models.DateField(blank=True, null=True)
    post_address = models.CharField(max_length=200, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.CharField(max_length=50, blank=True)

    ffrs_status = models.CharField(max_length=8, choices=FFRS_CHOICES, default='PSquad')
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='P')

    submitted = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

    def birth_date_short(self):
        return self.birth_date.strftime('%Y-%m-%d')

    def subscription_dues(self):
        dues = 10
        return dues

    def __str__(self):
        return "%s (#%s)" % (self.profile.derby_name, self.profile.derby_number)


class ProfileGroup(models.Model):
    name = models.CharField(max_length=200)
    profiles = models.ManyToManyField(Profile)

    def user_count(self):
        return self.profiles.count()

    def __str__(self):
        return "%s (%s)" % (self.name, self.profiles.count())
