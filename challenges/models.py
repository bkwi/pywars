from django.db import models
from django.conf import settings

from main.utils import _gen_id


class Challenge(models.Model):

    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    initial_code = models.TextField()
    solution = models.TextField()
    tests = models.TextField()
    points = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return '/challenge/%s' % self.pk

    def tests_as_list_of_strings(self):
        li = self.tests.split('\n')
        return [x.strip() for x in li if x]


class Solution(models.Model):

    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    challenge_id = models.CharField(max_length=16)
    code = models.TextField()
    votes_count = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='solutions', null=False)


class Vote(models.Model):

    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    solution = models.ForeignKey(Solution, related_name='votes', null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

