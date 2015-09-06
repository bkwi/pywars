from django.conf import settings

from .celery import app
from main.utils import push

import subprocess
import json

@app.task()
def save_code(code):
    with open('/home/vagrant/pywars/temp.py', 'w') as f:
        f.write(code)

@app.task()
def run(code, challenge_id, user_id):
    fname = '{}_{}'.format(challenge_id, user_id)
    with open('/home/vagrant/pywars/tempfiles/%s.py' % fname, 'w') as f:
        f.write(code)

    result = subprocess.check_output(
                 ['python',
                  '/home/vagrant/pywars/tempfiles/%s.py' % fname]
             ).strip()

    with open('/home/vagrant/pywars/tempfiles/result', 'w') as f:
        f.write(str(result))

    channel_name = settings.PUSHER_CHANNEL.format(user_id)

    result = json.loads(result)

    push.trigger(channel_name, 'test_result', result)
