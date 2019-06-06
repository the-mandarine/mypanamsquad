from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from opinions.models import OpinionQuestion, Opinion
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

def can_see_answers(user, opinion_question):
    user_in_allowed_group = any([user.profile in p_g.profiles.all() for p_g in opinion_question.group_can_see_answers.all()])
    user_is_allowed = user.profile in opinion_question.can_see_answers.all()
    return user_is_allowed or user_in_allowed_group

@user_passes_test(has_been_checked, login_url='/')
def index(request):
    user = request.user
    now = TZ.localize(datetime.now())
    opinion_questions = OpinionQuestion.objects.filter()
    context = {'opinion_questions': opinion_questions}
    return render(request, 'opinions/index.html', context)

@user_passes_test(has_been_checked, login_url='/login/')
def detail(request, slug):
    now = TZ.localize(datetime.now())
    opinion_question = get_object_or_404(OpinionQuestion, slug=slug)
    has_answered = request.user.profile in opinion_question.has_answered.all()
    user = request.user
    return render(request, 'opinions/detail.html', {
        'opinion_question': opinion_question,
        'has_answered': has_answered,
        'can_see_answers': can_see_answers(user, opinion_question)
    })

@user_passes_test(has_been_checked, login_url='/')
def express(request, slug):
    now = TZ.localize(datetime.now())
    opinion_question = get_object_or_404(OpinionQuestion, slug=slug)
    answer_text = request.POST['answer_text']
    answer_date = datetime.now()
    if request.user.profile not in opinion_question.has_answered.all():
        opinion = Opinion()
        opinion.question = opinion_question
        opinion.date = answer_date
        opinion.text = answer_text
        opinion.save()
        opinion_question.has_answered.add(request.user.profile)
    return HttpResponseRedirect(reverse('opinions:detail', args=(slug,)))

@user_passes_test(has_been_checked, login_url='/')
def results(request, slug):
    now = TZ.localize(datetime.now())
    opinion_question = get_object_or_404(OpinionQuestion, slug=slug)
    user = request.user
    if can_see_answers(user, opinion_question):
        return render(request, 'opinions/results.html', {'opinion_question': opinion_question})
    else:
        return HttpResponseRedirect(reverse('opinions:detail', args=(slug,)))

