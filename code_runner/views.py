import json
import pickle
import base64
import os
import sys
import hashlib
import uuid
from string import Template


import tornado.ioloop
from multiprocessing.pool import ThreadPool
from utils import test_code_template, validation_code, output_separator, logger
from dockerizer import DockerContainer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')

from django.conf import settings

_workers = ThreadPool(10)


class WebSocketResponseException(Exception):
    pass


class WebSocketResponse(object):

    response = None

    def __init__(self, msg, callback_socket):
        self.msg = msg
        self.msg_id = uuid.uuid4().hex
        logger.debug("Websocket message - id: %s, body: %s",
                     self.msg_id, msg)
        self.callback_socket = callback_socket
        self.perform()

    def perform(self):
        self.send_response()

    def send_response(self):
        if self.response is None:
            raise WebSocketResponseException('No response defined')
        logger.debug('Websocket response to %s: %s', self.msg_id,
                     self.response)
        self.callback_socket.write_message(self.response)


class Init(WebSocketResponse):
    response = {'action': 'init', 'msg': 'ok'}


class TestSolution(WebSocketResponse):
    response = {'action': 'test_queued', 'msg': 'queued'}

    def perform(self):
        super(TestSolution, self).perform()
        self.run_code(self.msg, callback=self.send_test_result)

    def send_test_result(self, resp):
        self.response = resp
        self.send_response()

    def run_code(self, data, callback, kwds={}):
        def _callback(result):
            tornado.ioloop.IOLoop.instance().\
                        add_callback(lambda: callback(result))
        _workers.apply_async(self.run, (data,), kwds, _callback)

    def run(self, data):
        challenge_id = data.get('challengeId')
        user_id = data.get('userId')
        solution = data.get('solution')
        tests = pickle.loads(base64.decodestring(data.get('tests')))

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
            logger.debug("[%s] Code not valid", self.msg_id)
            return result
        logger.debug("[%s] Code valid", self.msg_id)

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

