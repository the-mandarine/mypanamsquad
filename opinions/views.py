from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from opinions.models import OpinionQuestion, OpinionSubQuestion, Opinion
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

@user_passes_test(has_been_checked, login_url='/login/')
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
    subquestions = OpinionSubQuestion.objects.filter(question=opinion_question)
    can_answer = request.user.profile in opinion_question.can_answer.all()
    has_answered = request.user.profile in opinion_question.has_answered.all()
    user = request.user
    return render(request, 'opinions/detail.html', {
        'opinion_question': opinion_question,
        'subquestions': subquestions,
        'has_answered': has_answered,
        'can_answer': can_answer,
        'can_see_answers': can_see_answers(user, opinion_question)
    })

@user_passes_test(has_been_checked, login_url='/login/')
def express(request, slug):
    now = TZ.localize(datetime.now())
    opinion_question = get_object_or_404(OpinionQuestion, slug=slug)
    answer_text = request.POST.getlist('answer_text[]')
    stored_answer = answer_text
    if len(answer_text) >= 2:
        stored_answer = ""
        for field in answer_text:
            if field[:3] != 'Q: ':
                stored_answer += 'A: '+field
            else:
                stored_answer += field
            stored_answer += '\n'

    answer_date = datetime.now()
    if request.user.profile in opinion_question.can_answer.all() and request.user.profile not in opinion_question.has_answered.all():
        opinion = Opinion()
        opinion.question = opinion_question
        opinion.date = answer_date
        opinion.text = stored_answer
        opinion.save()
        opinion_question.has_answered.add(request.user.profile)
        opinion_question.save()
    return HttpResponseRedirect(reverse('opinions:detail', args=(slug,)))

@user_passes_test(has_been_checked, login_url='/login/')
def results(request, slug):
    now = TZ.localize(datetime.now())
    opinion_question = get_object_or_404(OpinionQuestion, slug=slug)
    user = request.user
    if can_see_answers(user, opinion_question):
        return render(request, 'opinions/results.html', {'opinion_question': opinion_question})
    else:
        return HttpResponseRedirect(reverse('opinions:detail', args=(slug,)))

