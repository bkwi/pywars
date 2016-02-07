import sys
import os

output_separator = '---json-response-below---'

test_code_template = '''
import json
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

$solution

statements = $test_statements

response = {'passed': True, 'msg': '', 'action': 'test_result'}

for statement in statements:
    try:
        with time_limit(2):
            if eval(statement) is not True:
                raise Exception('Statement %s is not True' % statement)
    except Exception as e:
        response['passed'] = False
        response['msg'] = e.message
        break

print '$separator'
print json.dumps(response)
'''

validation_code = '''$solution

import json

print '$separator'
print json.dumps({'valid': True})
'''
