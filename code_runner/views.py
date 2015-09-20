import json
import pickle
import base64
import os
import sys
import hashlib
from string import Template


import tornado.ioloop
from multiprocessing.pool import ThreadPool
from utils import code_template, output_separator
from dockerizer import DockerContainer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pywars.settings')


_workers = ThreadPool(10)


class WebSocketResponseException(Exception):
    pass


class WebSocketResponse(object):

    response = None

    def __init__(self, msg, callback_socket):
        self.msg = msg
        self.callback_socket = callback_socket
        self.perform()

    def perform(self):
        self.send_response()

    def send_response(self):
        if self.response is None:
            raise WebSocketResponseException('No response defined')
        self.callback_socket.write_message(self.response)


class Init(WebSocketResponse):
    response = {'action': 'init', 'msg': 'ok'}


class TestSolution(WebSocketResponse):
    response = {'action': 'test_solution', 'msg': 'queued'}

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

        fname = '{}_{}'.format(challenge_id, user_id)
        code = Template(code_template)
        code = code.substitute(solution=solution,
                        test_statements=tests,
                        separator=output_separator)

        with open('/home/vagrant/pywars/tempfiles/%s.py' % fname, 'w') as f:
            f.write(code)

        with DockerContainer(fname) as dc:
            result = dc.run()

        if result.get('passed'):
            token = hashlib.sha224(challenge_id + user_id).hexdigest()
            result['solution_token'] = token

        return result

