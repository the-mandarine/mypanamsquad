from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from derby.models import Player
from datetime import datetime

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

@user_passes_test(has_been_checked, login_url='/')
def index(request):
    context = {}
    return render(request, 'derby/index.html', context)

def presences(request):
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'presences/index.html', context)
