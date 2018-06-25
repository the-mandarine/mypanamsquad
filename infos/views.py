from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from infos.models import Profile
from datetime import datetime
from django.conf import settings

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

@login_required
def profile(request):
    """Edit my profile"""
    user = request.user
    context = {'user': user, 'edit_mode': True}
    return render(request, 'infos/profile.html', context)

@login_required
def success(request):
    user = request.user
    success_msg = "Merci d'avoir créé ton profil !"
    context = {'success_message': success_msg}
    return render(request, 'infos/profile.html', context)

@user_passes_test(has_been_checked, login_url='/')
def teammate(request, derby_number):
    """Check my teammate's profile"""
    return render(request, 'infos/teammate.html', {'user':user, 'edit_mode': False})

@login_required
def create(request):
    derby_name = pk=request.POST['derby_name']
    derby_number = pk=request.POST['derby_number']
    real_name = pk=request.POST['real_name']
    if not all((derby_name, derby_number, real_name,)):
        error_msg = "Tous les champs sont obligatoires."
        return render(request, 'infos/profile.html', {'error_message': error_msg})

    profile = Profile()
    profile.user = request.user
    profile.derby_name = derby_name
    profile.derby_number = derby_number
    profile.real_name = real_name
    profile.save()
    return HttpResponseRedirect(reverse('profile:success'))


@login_required
def edit(request):
    return HttpResponseRedirect(reverse('profile:success'))
