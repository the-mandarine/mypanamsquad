from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from derby.models import Training, TrainingPart, Player
from infos.models import Profile, ProfileGroup, Member
from datetime import date, datetime, timedelta
from PIL import Image
from io import StringIO, BytesIO
import os

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

def _is_member(user):
    valid = False
    try:
        valid = user.profile.member.has_been_processed
    except:
        valid = False
    return valid

def _can_validate_presences(user):
    valid = False
    usergroups = []
    try:
        group = ProfileGroup.objects.get(name='_can_validate_presences')
        usergroups = user.profile.profilegroup_set.all()
        valid = group in usergroups
    except:
        valid = False
    return valid

def profile(request, err = None, succ = None, info = None, emergency = None, captain = None, various = None):
    user = request.user
    context = {
                'user': user,
                'edit_mode': True,
                'default_photo_url': Player.DEFAULT_PHOTO,
                'default_photo2_url': Player.DEFAULT_PHOTO2
              }
    context.update({'emergency_infos': emergency, 'captain_infos': captain, 'various_infos': various})
    context.update({'error_message': err, 'success_message': succ, 'info_message': info})
    return render(request, 'derby/profile.html', context)

def profile_update(request):
    photo = request.FILES.get('photo', None)
    photo2 = request.FILES.get('photo2', None)
    emergency_infos = request.POST['emergency_infos']
    captain_infos = request.POST['captain_infos']
    various_infos = request.POST['various_infos']
    rgpd_consent = request.POST.getlist('rgpd_consent')
    try:
        player = Player.objects.get(profile=request.user.profile)
    except:
        player = Player()
        player.profile = request.user.profile

    if photo:
        photo_file = photo.file
        ima = Image.open(photo.file.name)
        ima.thumbnail((400, 600), Image.ANTIALIAS)
        imb = ima.convert('RGB')
        imb.save(photo_file, 'JPEG', quality=100)
        photo.file = photo_file
        player.photo = photo
        _, extension = os.path.splitext(photo.name)
        player.photo.name = "%s%s" % (request.user.profile.slug(), extension)
    if photo2:
        photo_file = photo2.file
        ima = Image.open(photo2.file.name)
        ima.thumbnail((400, 600), Image.ANTIALIAS)
        imb = ima.convert('RGB')
        imb.save(photo_file, 'JPEG', quality=100)
        photo2.file = photo_file
        player.photo2 = photo2
        _, extension = os.path.splitext(photo.name)
        player.photo2.name = "%s_2%s" % (request.user.profile.slug(), extension)
    player.save()

# Health part
    if not 'ok' in rgpd_consent:
        return profile(request,
                       err="Les données n'ont pas été sauvegardées. L'acceptation du traitement des données par la Panam Squad est nécessaire.",
                       emergency=emergency_infos, 
                       captain=captain_infos,
                       various=various_infos)

    player.emergency_infos = emergency_infos
    player.captain_infos = captain_infos
    player.various_infos = various_infos
    player.save()

    return profile(request, succ="Profile derby mis à jour")

@user_passes_test(has_been_checked, login_url='/')
def trainings(request):
    trainings = Training.objects.filter(date__gte=datetime.now()-timedelta(days=30), date__lt=datetime.now()+timedelta(days=15)).order_by('-date')
    context = {'trainings': trainings}
    return render(request, 'training/index.html', context)

@user_passes_test(_is_member, login_url='/')
def training(request, date):
    try:
        train = Training.objects.get(date=date)
    except Training.DoesNotExist:
        train = Training.objects.last()
        return HttpResponseRedirect(reverse('derby:training', args=(train.date,)))
    players = Player.objects.all().order_by('profile__derby_number')
    context = {
                'default_photo': Player.DEFAULT_PHOTO,
                'training': train,
                'players': players
              }
    return render(request, 'training/detail.html', context)

@user_passes_test(_can_validate_presences, login_url='/')
def presences(request):
    training_id = request.POST['training_id']
    clear_parts = request.POST.get('clear_parts', None)
    train = Training.objects.get(id = training_id)

    if clear_parts == training_id:
        for part in train.parts.all():
            part.people.clear()
    
    for post_var in request.POST.keys():
        if post_var.startswith('pres_'):
            part_player_id = post_var[5:]
            part_id, player_id = part_player_id.split('_')
            player = Player.objects.get(id=player_id)
            part = TrainingPart.objects.get(id=part_id)
            if request.POST[post_var] == 'Y':
                part.people.add(player)
                part.save()

    return HttpResponseRedirect(reverse('derby:training', args=(train.date,)))

