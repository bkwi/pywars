from django.db import models

from main.utils import _gen_id


class Challenge(models.Model):

    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    initial_code = models.TextField()
    solution = models.TextField()
    tests = models.TextField()

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return '/challenge/%s' % self.pk
