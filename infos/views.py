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

@user_passes_test(has_been_checked, login_url='/')
def teammate(request, derby_number):
    """Check my teammate's profile"""
    return render(request, 'infos/teammate.html', {'vote': vote, 'activated': True})

@login_required
def base_edit(request):
    selected = vote.voteitem_set.get(pk=request.POST['vote'])
    selected.save()
    return HttpResponseRedirect(reverse('votes:detail', args=(slug,)))


@login_required
def edit(request):
    selected = vote.voteitem_set.get(pk=request.POST['vote'])
    selected.save()
    return HttpResponseRedirect(reverse('votes:detail', args=(slug,)))
