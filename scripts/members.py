#!/usr/bin/env python
from infos.models import Member

players = Member.objects.filter(role='P').count()
coachs = Member.objects.filter(role='C').count()
officials = Member.objects.filter(role='O').count()

print (players, "players")
print (coachs, "coachs")
print (officials, "officials")

