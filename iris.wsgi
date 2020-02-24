import sys, logging

sys.path.append('/var/www/iris_app')

activate_this = '/var/www/iris_app/venv/bin/activate_this.py'

def exec_full(filepath):
    import os
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
        }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)

exec_full(activate_this)

from iris import app as application
logging.basicConfig(stream = sys.stderr)

