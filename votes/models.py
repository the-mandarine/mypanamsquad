from django.db import models
from django.contrib.auth.models import User
from infos.models import Profile, ProfileGroup
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.db.models import Max

TZ = timezone(settings.TIME_ZONE)

# Create your models here.
class Vote(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(max_length=4000)
    can_vote = models.ManyToManyField(Profile, related_name='can_vote_for', blank=True)
    group_can_vote = models.ManyToManyField(ProfileGroup, related_name='can_vote_for', blank=True)
    has_voted = models.ManyToManyField(Profile, related_name='voted_for', blank=True, editable=False)
    pub_date = models.DateTimeField('date published', blank=True, default=datetime.now)
    end_date = models.DateTimeField('end date', blank=True, default=datetime.now)
    def __str__(self):
        return self.name

    def is_open(self):
        now = TZ.localize(datetime.now())
        return self.end_date > now

    def get_vote_status(self):
        return "%i/%i" % (self.has_voted.count(), len(self.get_voters()))
    get_vote_status.short_description = 'Vote status'

    def get_percent_voting(self):
        return int(100 * self.has_voted.count() / len(self.get_voters()))

    def get_voters(self):
        voters = set(self.can_vote.all())
        for profile_group in self.group_can_vote.all():
            for profile in profile_group.profiles.all():
                voters.add(profile)
        return voters

    def get_voters_count(self):
        return len(self.get_voters())

class VoteItem(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    results = models.IntegerField(default=0, editable=False)
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


        
