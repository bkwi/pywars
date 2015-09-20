import docker
import json
import re

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings

from utils import output_separator


class DockerContainer(object):

    def __init__(self, container_id):
        self.cid = container_id
        self.client = docker.Client(base_url='unix://var/run/docker.sock')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.remove_container(self.cid)

    def run(self):
        try:
            self.container = self.client.create_container(
                image='python:2.7',
                command="python /mnt/temp/%s.py" % self.cid,
                name=self.cid,
                host_config=self.client.create_host_config(
                    binds={settings.TEMPFILES_PATH: {'bind': '/mnt/temp/',
                                                     'mode': 'rw'}}))

            self.client.start(self.cid)
            self.client.wait(self.cid)
            output = self.client.logs(self.cid)
            result = output.split(output_separator)[-1].strip()
            try:
                return json.loads(result)
            except:
                # Remove file path from traceback
                output = re.sub(r'(?ms)File "\/mnt.*\.py",', 'In', output)
                return {'passed': False, 'msg': output,
                        'action': 'test_result'}
        except Exception as e:
            # TODO
            raise e
