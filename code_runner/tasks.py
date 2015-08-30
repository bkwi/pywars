from .celery import app
from main.utils import push

import subprocess
import json

@app.task()
def save_code(code):
    with open('/home/vagrant/pywars/temp.py', 'w') as f:
        f.write(code)

@app.task()
def run(code):
    with open('/home/vagrant/pywars/tempfiles/temp.py', 'w') as f:
        f.write(code)

    result = subprocess.check_output(
                 ['python',
                  '/home/vagrant/pywars/tempfiles/temp.py']
             ).strip()

    with open('/home/vagrant/pywars/tempfiles/result', 'w') as f:
        f.write(str(result))

    push.trigger('test_channel', 'test_result', json.loads(result))
