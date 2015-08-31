from django.conf import settings

import os

import pusher

def _gen_id():
    """
    Used to generate random 16-character ids for models
    """
    return os.urandom(16).encode('hex')[:16]

push = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                     key=settings.PUSHER_KEY,
                     secret=settings.PUSHER_SECRET,
                     ssl=True,
                     port=443)
