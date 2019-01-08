# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required
def home(request):
    try:
        profile = request.user.profile
    except:
        return HttpResponseRedirect(reverse('profile:profile'))
    can_validate_paid = profile.profilegroup_set.filter(name='_can_validate_paid').exists()
    can_see_variousinfos = profile.profilegroup_set.filter(name='_can_see_variousinfos').exists()
    context = {
               'can_validate_paid': can_validate_paid,
               'can_see_variousinfos': can_see_variousinfos}
    return render(request, 'core/home.html', context)

def privacy(request):
    return render(request, 'core/privacy.html')
