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
    return render(request, 'core/home.html')

def privacy(request):
    return render(request, 'core/privacy.html')
