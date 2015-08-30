from django.contrib.auth.decorators import login_required
from django.conf import settings

import os

import pusher


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

def _gen_id():
    """
    Used to generate random 16-character ids for models
    """
    return os.urandom(16).encode('hex')[:16]

push = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  ssl=True,
  port=443
)
