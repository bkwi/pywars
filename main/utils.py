from django.contrib.auth.decorators import login_required

import os

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
