from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from votes.models import Vote, VoteItem
from datetime import datetime
from pytz import timezone
from django.conf import settings

TZ = timezone(settings.TIME_ZONE)

def has_been_checked(user):
    valid = False
    try:
        valid = user.profile.has_been_checked
    except:
        valid = False
    return valid

@user_passes_test(has_been_checked, login_url='/')
def index(request):
    user = request.user
    now = TZ.localize(datetime.now())
    latest_votes = Vote.objects.filter(pub_date__lt=now).order_by('-end_date')
    context = {'latest_votes': latest_votes}
    return render(request, 'votes/index.html', context)

@user_passes_test(has_been_checked, login_url='/')
def detail(request, slug):
    now = TZ.localize(datetime.now())
    vote = get_object_or_404(Vote, slug=slug, pub_date__lt=now)
    if vote.end_date < now or vote.has_voted.count() == vote.get_voters_count():
        return HttpResponseRedirect(reverse('votes:results', args=(slug,)))
    if request.user.profile not in vote.get_voters():
        return render(request, 'votes/detail.html', {
            'vote': vote,
            'error_message': "Il t'est impossible de voter sur ce sujet.",
            'activated': False
        })
    if vote.end_date < now or vote.has_voted.count() == vote.get_voters_count():
        return HttpResponseRedirect(reverse('votes:results', args=(slug,)))
    elif request.user.profile in vote.has_voted.all():
        return render(request, 'votes/detail.html', {
            'vote': vote,
            'error_message': "Merci d'avoir voté ! Les résultats paraîtront bientôt.",
            'activated': False
        })
    return render(request, 'votes/detail.html', {'vote': vote, 'activated': True})

@user_passes_test(has_been_checked, login_url='/')
def vote(request, slug):
    now = TZ.localize(datetime.now())
    vote = get_object_or_404(Vote, slug=slug, pub_date__lt=now)
    try:
        selected = vote.voteitem_set.get(pk=request.POST['vote'])
        assert request.user.profile in vote.get_voters()
        assert request.user.profile not in vote.has_voted.all()
    except (KeyError, VoteItem.DoesNotExist):
        return render(request, 'votes/detail.html', {
            'vote': vote,
            'error_message': "Il faut sélectionner un choix.",
            'activated': True
        })
    except AssertionError:
        return render(request, 'votes/detail.html', {
            'vote': vote,
            'error_message': "Tu ne peux pas voter là dessus ou tu l'as déjà fait.",
            'activated': False,
        })
    else:
        vote.has_voted.add(request.user.profile)
        selected.results += 1
        selected.save()
    return HttpResponseRedirect(reverse('votes:detail', args=(slug,)))

@user_passes_test(has_been_checked, login_url='/')
def results(request, slug):
    now = TZ.localize(datetime.now())
    vote = get_object_or_404(Vote, slug=slug)
    if vote.end_date > now and vote.has_voted.count() < vote.get_voters_count():
        return HttpResponseRedirect(reverse('votes:detail', args=(slug,)))
    return render(request, 'votes/results.html', {'vote': vote})

