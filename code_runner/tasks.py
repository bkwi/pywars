from .celery import app

@app.task()
def save_code(code):
    with open('/home/vagrant/pywars/temp.py', 'w') as f:
        f.write(code)
