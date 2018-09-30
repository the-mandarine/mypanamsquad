#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "..panamsquad.settings")
import django
django.setup()

from infos.models import Member

players = Member.objects.filter(role='P').count()
coachs = Member.objects.filter(role='C').count()
officials = Member.objects.filter(role='O').count()

print (players, "players")
print (coachs, "coachs")
print (officials, "officials")

