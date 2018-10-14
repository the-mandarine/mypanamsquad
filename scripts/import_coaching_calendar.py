#!/usr/bin/env python

from datetime import datetime, timedelta, timezone, date
import icalendar
from dateutil.rrule import *
from bs4 import BeautifulSoup

import requests
import json
from derby.models import Training, TrainingPart, Place

CAL_URL="https://calendar.google.com/calendar/ical/b2ik774ulttp27h55osjhbble8%40group.calendar.google.com/public/basic.ics"

def parse_recurrences(recur_rule, start, exclusions):
    """ Find all reoccuring events """
    from dateutil.rrule import rruleset, rrulestr
    from datetime import datetime, timedelta, timezone, date, time
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=start)
    rules.rrule(first_rule)
    if not isinstance(exclusions, list):
        exclusions = [exclusions]
        for xdate in exclusions:
            try:
                rules.exdate(xdate.dts[0].dt)
            except AttributeError:
                pass
    now = datetime(2018, 8, 25, 0, 0, tzinfo=timezone.utc)
    this_year = now + timedelta(days=300)
    dates = []
    try:
        for rule in rules.between(now, this_year):
            dates.append(rule.strftime("%Y-%m-%d"))
    except:
        pass
    return dates

calendar = icalendar.Calendar.from_ical(requests.get(CAL_URL).text)
trainings = {}
disp=False
for event in calendar.walk():
    if event.name == "VEVENT" and event.get('dtstart'):
        startdt = event.get('dtstart').dt
        enddt = event.get('dtend').dt
        exdate = event.get('exdate')
        if type(startdt) is date:
            event_dates = [str(event.get('dtstart').dt)]
        elif type(startdt) is datetime:
            event_dates = [str(event.get('dtstart').dt.date())]

        
        if event.get('rrule'):
            reoccur = event.get('rrule').to_ical().decode('utf-8')
            event_dates = []
            for item in parse_recurrences(reoccur, startdt, exdate):
                event_dates.append(str(item))

        for event_date in event_dates:
            training = trainings.get(event_date, {})
            t_part = training.get(event.get('summary'), "")
            if "Louis Braille" not in event.get('summary') and "Mac Do" not in event.get('summary'):
                print(repr(event.get('summary')))
                if t_part:
                    t_part += "\n"
                t_part += BeautifulSoup(event.get('description')).get_text()
                training[event.get('summary')] = t_part
                trainings[event_date] = training


for training_date in trainings:
    training = Training.objects.filter(date=training_date).last()
    if not training:
        training = Training()
        training.date = datetime.strptime(training_date, '%Y-%m-%d')

    mcdo = Place.objects.get(short_name="MacDo")
    braille = Place.objects.get(short_name="Braille")
    if training.date.weekday() == 5:
        training.place = mcdo
    elif training.date.weekday() == 1:
        training.place = braille
    training.save()

    for name in trainings[training_date]:
        desc = trainings[training_date][name]
        try:
            part = TrainingPart.objects.get(training=training, name=name)
        except:
            part = TrainingPart()
            part.training = training
            part.name = name
        part.desc = desc
        part.save()
    training.save()

