from django.conf import settings

import os
import hashlib

import pusher

def _gen_id():
    """
    Used to generate random 16-character ids for models
    """
    return os.urandom(16).encode('hex')[:16]

def encrypt(string_data):
    return hashlib.sha224(string_data + settings.SECRET_KEY).hexdigest()

push = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                     key=settings.PUSHER_KEY,
                     secret=settings.PUSHER_SECRET,
                     ssl=True,
                     port=443)
