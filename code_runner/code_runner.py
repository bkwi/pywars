import tornado.ioloop
import tornado.web
import tornado.websocket

import json
import pickle
import base64
import os
import hashlib
from string import Template

from multiprocessing.pool import ThreadPool

from utils import code_template

_workers = ThreadPool(10)

def run(data):

    challenge_id = data.get('challengeId')
    user_id = data.get('userId')
    solution = data.get('solution')
    tests = pickle.loads(base64.decodestring(data.get('tests')))

    fname = '{}_{}'.format(challenge_id, user_id)
    code = Template(code_template)
    code = code.substitute(solution=solution,
                    test_statements=tests)

    with open('/home/vagrant/pywars/tempfiles/%s.py' % fname, 'w') as f:
        f.write(code)

    result = os.popen('python {}'.format(
        '/home/vagrant/pywars/tempfiles/%s.py' % fname)).read()

    result = json.loads(result)
    if result.get('passed'):
        token = hashlib.sha224(challenge_id + user_id).hexdigest()
        result['solution_token'] = token

    return result

def run_code(data, callback, kwds={}):
    def _callback(result):
        tornado.ioloop.IOLoop.instance().\
                    add_callback(lambda: callback(result))
    _workers.apply_async(run, (data,), kwds, _callback)


class PyWarsApi(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"

    @tornado.web.asynchronous
    def on_message(self, message):
        data = json.loads(message)
        action = data.get('action')
        print data
        if action == 'init':
            response = {'code': 200, 'action': 'init', 'msg': 'OK'}
            self.write_message(json.dumps(response))
        elif action == 'test_solution':
            run_code(data, callback=self.write_message)
            response = {'code': 200, 'action': 'test_solution',
                        'msg': 'queued'}
            self.write_message(response)

    def on_close(self):
        print "WebSocket closed"

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r"/websocket", PyWarsApi)
])

if __name__ == "__main__":
    application.listen(4444)
    tornado.ioloop.IOLoop.instance().start()

