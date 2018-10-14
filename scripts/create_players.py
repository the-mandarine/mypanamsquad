#!/usr/bin/env python
from infos.models import Member
from derby.models import Player

players = Member.objects.filter(role='P')

for player in players:
    try:
        p = Player.objects.get(profile=player.profile)
    except:
        p = Player()
        p.profile = player.profile
        p.save()

