from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.db.models import Max

TZ = timezone(settings.TIME_ZONE)

# Create your models here.
class Vote(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=400)
    can_vote = models.ManyToManyField(User, related_name='can_vote_for', blank=True)
    has_voted = models.ManyToManyField(User, related_name='voted_for', blank=True)
    pub_date = models.DateTimeField('date published', blank=True, default=datetime.now)
    end_date = models.DateTimeField('end date', blank=True, default=datetime.now)
    def __str__(self):
        return self.name

    def is_open(self):
        now = TZ.localize(datetime.now())
        return self.end_date > now

    def get_vote_status(self):
        return "%i/%i" % (self.has_voted.count(), self.can_vote.count())
    get_vote_status.short_description = 'Vote status'

    def get_percent_voting(self):
        return int(100 * self.has_voted.count() / self.can_vote.count())

class VoteItem(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    results = models.IntegerField(default=0, editable=True)
    def __str__(self):
        return self.text

    def get_percent_voted(self):
        results = self.vote.voteitem_set.all().aggregate(Max('results'))
        result_max = results['results__max']
        return int(8 + 92 * self.results / (result_max))

    def has_won(self):
        all_votes_items = self.vote.voteitem_set.all()
        for item in all_votes_items:
            if item.results > self.results:
                return False
        return True

    def has_equal(self):
        all_votes_items = self.vote.voteitem_set.all()
        for item in all_votes_items:
            if item.results == self.results and item.text != self.text:
                return True
        return False


        
