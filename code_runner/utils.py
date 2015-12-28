import sys
import os
import logging
import logging.config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings

logger = logging.getLogger('tornado')
logging.config.dictConfig(settings.LOGGING)