from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from infos.models import Profile, ProfileGroup, Member
from datetime import datetime
from django.conf import settings

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

def has_membership(user):
    valid = False
    try:
        valid = bool(user.profile.member)
    except:
        valid = False
    return valid

def _can_validate_paid(user):
    valid = False
    group = ProfileGroup.objects.get(name='_can_validate_paid')
    usergroups = []
    try:
        usergroups = user.profile.profilegroup_set.all()
        valid = group in usergroups
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
def membership(request, err=None, succ=None, info=None):
    """Edit my panamsquad membership"""
    user = request.user
    roles = Member.ROLE_CHOICES
    ffrs = Member.FFRS_CHOICES
    context = {'user': user, 'edit_mode': True, 'roles': roles, 'ffrs': ffrs}
    context.update({'error_message': err, 'success_message': succ, 'info_message': info})
    return render(request, 'infos/membership.html', context)

@login_required
def success(request):
    user = request.user
    success_msg = "Merci d'avoir créé ton profil !"
    context = {'success_message': success_msg}
    return render(request, 'infos/profile.html', context)

@user_passes_test(has_been_checked)
def index(request):
    members = Member.objects.filter().order_by('role')
    return render(request, 'infos/index.html', {'members': members, 'filter_name': "adhérents"})

@user_passes_test(has_been_checked)
def memberlist(request):
    members = Member.objects.filter(submitted=True, has_paid=True).order_by('role')
    return render(request, 'infos/index.html', {'members': members, 'filter_name': "adhérents"})

@user_passes_test(has_been_checked)
def teammate(request, derby_number):
    """Check my teammate's profile"""
    user = request.user
    return render(request, 'infos/teammate.html', {'user': user, 'edit_mode': False})

@login_required
def create(request):
    derby_name = pk=request.POST['derby_name']
    derby_number = pk=request.POST['derby_number']
    if not derby_number:
        derby_number = '____'

    if not all((derby_name, derby_number,)):
        error_msg = "Il est nécessaire de renseigner un derby name."
        return render(request, 'infos/profile.html', {'error_message': error_msg})

    profile = Profile()
    profile.user = request.user
    profile.derby_name = derby_name
    profile.derby_number = derby_number
    profile.save()
    return HttpResponseRedirect(reverse('profile:success'))

@login_required
def subscribe(request):
    real_name = request.POST['real_name']
    birth_date = request.POST['birth_date']
    post_address = request.POST['post_address']
    postal_code = request.POST['postal_code']
    city = request.POST['city']
    contact_phone = request.POST['contact_phone']
    contact_email = request.POST['contact_email']
    role = request.POST['role']
    ffrs_status = request.POST['ffrs_status']
    save = bool(request.POST.get('save', False))
    submit = bool(request.POST.get('submit', False))
    data_ok = bool(request.POST.get('data_ok', False))
    ri_ok = bool(request.POST.get('ri_ok', False))
    health_cert = request.FILES.get('health_cert', None)
    keep_health_cert = bool(request.POST.get('keep_health_cert', False))
    try:
        member = Member.objects.get(profile=request.user.profile)
    except:
        member = Member()
        member.profile = request.user.profile

    member.real_name = real_name
    member.birth_date = birth_date
    member.post_address = post_address
    member.postal_code = postal_code
    member.city = city
    member.contact_phone = contact_phone
    member.contact_email = contact_email
    member.role = role
    member.ffrs_status = ffrs_status
    if health_cert:
        member.health_cert = health_cert
    member.keep_health_cert = keep_health_cert
    member.save()

    if submit:
    # Check that the mandatory box
        if not data_ok:
            error_msg = "Il faut accepter que la Panam Squad utilise les informations fournies pour adhérer."
            return membership(request, err=error_msg)
        if not ri_ok:
            error_msg = "Il faut accepter le Règlement Intérieur pour adhérer."
            return membership(request, err=error_msg)
        if member.ffrs_status in ('PComp',) and not member.health_cert:
            error_msg = "Il te faut avoir un certificat médical dans ton dossier pour acquérir ce type de license FFRS."
            return membership(request, err=error_msg)
        member.submitted = True
        member.save()
        msg = "Merci d'avoir transmis ton dossier."
        return membership(request, succ=msg)

    
    msg = "Ton dossier a bien été sauvegardé."
    return membership(request, succ=msg)

@login_required
def edit(request):
    return HttpResponseRedirect(reverse('profile:success'))

@user_passes_test(has_membership)
def health_cert_redir(request):
    member = request.user.profile.member
    if member.health_cert:
        cert_url = member.health_cert_url()
        return HttpResponseRedirect(reverse('profile:health_cert', args=(cert_url,)))
    return HttpResponseRedirect(reverse('profile:profile'))

@user_passes_test(has_been_checked)
def health_cert(request, filename):
    user = request.user
    cert_file = user.profile.member.health_cert
    return HttpResponse(cert_file.read(), content_type='application/octet-stream')

@user_passes_test(_can_validate_paid)
def validate_payments(request):
    for post_var in request.POST.keys():
        if post_var.startswith('paid_'):
            member_id = post_var[5:]
            member = Member.objects.get(id=member_id)
            print (member, repr(request.POST[post_var]))
            if request.POST[post_var] == 'Y':
                member.has_paid = True
            elif request.POST[post_var] == 'N':
                member.has_paid = False
            member.save()
    submitted_members = Member.objects.filter(submitted=True).order_by('profile__derby_name')
    msg = "Les paiements ont été enregistrés."
    context = {'submitted_members': submitted_members, 'success_message': msg}
    return render(request, 'infos/payments.html', context)

@user_passes_test(_can_validate_paid)
def payments(request):
    submitted_members = Member.objects.filter(submitted=True).order_by('has_paid', 'profile__derby_name')
    return render(request, 'infos/payments.html', {'submitted_members': submitted_members})

