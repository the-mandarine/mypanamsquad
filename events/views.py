from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from events.models import Event, Attendance
from infos.models import Profile
from datetime import datetime
from pytz import timezone
from django.conf import settings

TZ = timezone(settings.TIME_ZONE)
MAX_PROXY = 3

def get_proxies(event):
    profiles = event.expected_members.filter(has_been_checked = True).order_by('derby_name')
    for profile in profiles:
        profile.possible_proxy = True
        proxy_absent = Attendance.objects.filter(event = event, member = profile, attendance = 'N')
        proxy_from = Attendance.objects.filter(event = event, member = profile, attendance = 'P')
        proxy_to_count = Attendance.objects.filter(event = event, proxy_to = profile, attendance = 'P').count()
        if proxy_absent:
            #Proxy won't be there
            profile.possible_proxy = False
        if proxy_from:
            #Proxy already uses a proxy
            profile.possible_proxy = False
        if proxy_to_count >= MAX_PROXY:
            #Proxy is already used by 3 members
            profile.possible_proxy = False

        yield profile

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

@user_passes_test(has_been_checked)
def index(request):
    user = request.user
    now = TZ.localize(datetime.now())
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'events/index.html', context)

@user_passes_test(has_been_checked)
def detail(request, slug):
    now = TZ.localize(datetime.now())
    user = request.user
    event = get_object_or_404(Event, slug=slug)
    proxies = get_proxies(event)
    member_proxies = Attendance.objects.filter(event=event, proxy_to=user.profile)
    try:
        attendance = Attendance.objects.get(event=event, member=user.profile)
    except Attendance.DoesNotExist:
        attendance = Attendance(event=event, member=user.profile)
    return render(request, 'events/detail.html', {
        'event': event,
        'proxies': proxies,
        'member_proxies': member_proxies,
        'attendance': attendance,
    })

@user_passes_test(has_been_checked)
def attend(request, slug):
    now = TZ.localize(datetime.now())
    event = get_object_or_404(Event, slug=slug)
    user = request.user
    proxy_to = request.POST.get('proxy', None)
    present = request.POST.get('Y', False)
    proxy = request.POST.get('P', False)
    absent = request.POST.get('N', False)
    try:
        attendance = Attendance.objects.get(event=event, member=user.profile)
    except Attendance.DoesNotExist:
        attendance = Attendance(event=event, member=user.profile)
    if present:
        attendance.attendance = 'Y'
        attendance.proxy_to = None
        attendance.accepted = True
    elif proxy:
        attendance.attendance = 'P'
        try:
            proxy_profile = Profile.objects.get(pk = proxy_to)
        except Profile.DoesNotExist:
            attendance.attendance = 'N'
            proxy_profile = None
        attendance.proxy_to = proxy_profile
        attendance.accepted = False
        # Remove all proxy requests
        Attendance.objects.filter(event=event, proxy_to=user.profile).delete()
    else:
        attendance.attendance = 'N'
        attendance.proxy_to = None
        attendance.accepted = True
        # Remove all proxy requests
        Attendance.objects.filter(event=event, proxy_to=user.profile).delete()
        Attendance.objects.filter(event=event, member=user.profile).delete()

    attendance.save()
    return HttpResponseRedirect(reverse('events:detail', args=(slug,)))

@user_passes_test(has_been_checked)
def proxy(request, slug):
    now = TZ.localize(datetime.now())
    event = get_object_or_404(Event, slug=slug)
    member_id = request.POST.get('member_id', None)
    proxy_member = get_object_or_404(Profile, id=member_id)
    user = request.user
    try:
        attendance = Attendance.objects.get(event=event, member=proxy_member, proxy_to=user.profile)
    except Attendance.DoesNotExist:
        return HttpResponseRedirect(reverse('events:detail', args=(slug,)))

    accept = request.POST.get('proxy_accept', False)
    deny = request.POST.get('proxy_deny', False)
    if accept:
        attendance.accepted = True
        attendance.save()
        try:
            self_att = Attendance.objects.get(event=event, member=user.profile)
        except Attendance.DoesNotExist:
            self_att = Attendance(event=event, member=user.profile)
        self_att.attendance = 'Y'
        self_att.proxy_to = None
        self_att.accepted = True
        self_att.save()
    elif deny:
        attendance.delete()

    return HttpResponseRedirect(reverse('events:detail', args=(slug,)))

