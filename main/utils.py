from django.conf import settings

import os
import hashlib
import requests
import logging


logger = logging.getLogger('pywars')

def _gen_id():
    """
    Used to generate random 16-character ids for models
    """
    return os.urandom(16).encode('hex')[:16]

def encrypt(string_data):
    return hashlib.sha224(string_data).hexdigest()

def send_email(email_address, body, subject):
    if settings.DEBUG:
        logger.debug('Email skipped')
        logger.debug("TO: %s\nSubject: %s\n\n%s",
                     email_address, subject, body)
        return

    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % settings.MAILGUN_DOMAIN,
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": settings.FROM_FIELD,
              "to": [email_address],
              "subject": subject,
              "text": body})
