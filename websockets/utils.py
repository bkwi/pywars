import sys
import os
import logging
import logging.config
import hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings

logger = logging.getLogger('websockets')
logging.config.dictConfig(settings.LOGGING)

def authorize(headers):
    token = headers.get('Token', '')
    signature = headers.get('Signature', '')
    return signature == hashlib.sha224(token + settings.SECRET_KEY).hexdigest()