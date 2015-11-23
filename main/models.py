from django.db import models
from django.conf import settings

import json

from main.utils import _gen_id


class Notification(models.Model):
    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    notified_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      related_name='notifications')
    about = models.CharField(max_length=100)
    active = models.BooleanField()
    url_params = models.TextField()

    def url(self):
        params = json.loads(self.url_params)

        if self.about == 'comment':
            final_url = '/challenge/{}/solutions#{}'.format(
                    params.get('challenge_id'), params.get('solution_id'))
        else:
            final_url = '#'

        return final_url

    def body(self):
        params = json.loads(self.url_params)

        if self.about == 'comment':
            b = '{} commented on your solution'.format(
                           params.get('comment_author_name'))
        else:
            b = ''
        return b
