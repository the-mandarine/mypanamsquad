# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import unicodedata
import os
import string


# Create your models here.
class Profile(models.Model):

    # bypass for votes
    has_been_checked = models.BooleanField(default = False)

    # actual profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    derby_name = models.CharField(max_length=200)
    derby_number = models.CharField(max_length=5, blank=True)
    fb_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "%s (#%s)" % (self.derby_name, self.derby_number)

    def slug(self):
        return ''.join(e for e in str(self) if e.isalnum())

class Member(models.Model):
    FFRS_CHOICES = (('PComp', 'Licence "en patins" par la Panam Squad'),
                    ('PFoot', 'Licence "non-pratiquant" par la Panam Squad'),
                    ('NoLic', "Licence par un autre club ou pas besoin de licence FFRS"))

    ROLE_CHOICES = (('P', 'Jouer'),
                    ('O', 'Officier/Arbitrer'),
                    ('C', 'Coacher'),)

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=200)
    has_been_processed = models.BooleanField(default = False)
    birth_date = models.DateField(blank=True, null=True)
    post_address = models.CharField(max_length=200, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.CharField(max_length=50, blank=True)

    ffrs_status = models.CharField(max_length=8, choices=FFRS_CHOICES, default='PComp')
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='P')

    submitted = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

    health_cert = models.FileField(upload_to='health_certs', blank=True)
    keep_health_cert = models.BooleanField(default=False)

    def birth_date_short(self):
        try:
            value = self.birth_date.strftime('%Y-%m-%d')
        except:
            value = ""
        return value

    def subscription_dues(self):
        dues = 0
        if self.role in ('P',):
            dues += 75
        elif self.role in ('O', 'C',):
            dues += 10
        if self.ffrs_status in ('PComp', 'PFoot'):
            dues += 40
        return dues

    def health_cert_url(self):
        name = "%s%s" % (self.profile.derby_number, self.profile.derby_name)
        cert_name = unicodedata.normalize('NFKD', name).replace(' ', '')
        _, extension = os.path.splitext(self.health_cert.name)
        return cert_name+extension

    def display_name(self):
        return "%s (#%s)" % (self.profile.derby_name, self.profile.derby_number)

    display_name.short_description = 'Profile'

    def __str__(self):
        return self.display_name()


class ProfileGroup(models.Model):
    name = models.CharField(max_length=200)
    profiles = models.ManyToManyField(Profile)

    def user_count(self):
        return self.profiles.count()

    def __str__(self):
        return "%s (%s)" % (self.name, self.profiles.count())
