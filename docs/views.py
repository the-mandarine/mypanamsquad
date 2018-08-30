from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from docs.models import Doc
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
    docs = Doc.objects.all()
    context = {'docs': docs}
    return render(request, 'docs/index.html', context)

def detail(request, slug):
    doc = get_object_or_404(Doc, slug=slug)
    context = {'doc': doc}
    return render(request, 'docs/detail.html', context)

def redir(request, slug):
    doc = get_object_or_404(Doc, slug=slug)
    return HttpResponseRedirect('/' + doc.asset.url)

