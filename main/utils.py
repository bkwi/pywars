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
    return hashlib.sha224(string_data).hexdigest()

