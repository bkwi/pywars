from .celery import app

import subprocess

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
             )

    with open('/home/vagrant/pywars/tempfiles/result', 'w') as f:
        f.write(str(result))
