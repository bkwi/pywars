from __future__ import absolute_import
import os
from celery import Celery, task
import sys
import hashlib
import uuid
from string import Template

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings
from main.utils import logger


from challenges.docker_container import DockerContainer
from challenges.utils import test_code_template, validation_code, \
                             output_separator

app = Celery('code_runner')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def run_code(data):
    logger.info('Celery worker received data: %s', data)

    challenge_id = data.get('challengeId')
    user_id = data.get('userId')
    solution = data.get('solution')
    tests = data.get('tests')

    path = settings.TEMPFILES_PATH
    fname = '{}_{}'.format(challenge_id, user_id)

    # run solution only - check syntax errors etc.
    code = Template(validation_code)
    code = code.substitute(solution=solution,
                separator=output_separator)

    with open('{}/{}_validate.py'.format(path, fname) , 'w') as f:
        f.write(code)

    with DockerContainer(fname + '_validate') as dc:
        result = dc.run()

    if not result.get('valid'):
        logger.debug("Code not valid")
        return result
    logger.debug("Code valid")

    code = Template(test_code_template)
    code = code.substitute(solution=solution,
                           test_statements=tests,
                           separator=output_separator)

    with open('{}/{}.py'.format(path, fname) , 'w') as f:
        f.write(code)

    with DockerContainer(fname) as dc:
        result = dc.run()

    if result.get('passed'):
        token = hashlib.sha224(challenge_id + user_id).hexdigest()
        result['solution_token'] = token
    return result


@app.task(bind=True)
def run_and_notify(self, data):
    result = run_code(data)
    result['user_id'] = data.get('userId')
    token = uuid.uuid4().hex
    signature = hashlib.sha224(token + settings.SECRET_KEY).hexdigest()
    headers = {'token': token, 'signature': signature}
    requests.post(settings.NOTIFICATION_API_URL, json=result,
                  headers=headers)


