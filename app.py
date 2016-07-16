import os
import requests
import time
import bottle
from bottle import Bottle, redirect, route
from bottle import template, SimpleTemplate
from bottle import get, post, request, response
from urlparse import urlparse
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from functools import wraps

app = Bottle()

app_dir = os.path.dirname(os.path.abspath(__file__))

dir_executables = os.path.join(app_dir, "executables")

BENCHMARKS = {
    "linpack": os.path.join(dir_executables + "linpackbm.jar"),
    "prime": os.path.join(dir_executables + "prime.jar"),
    "image": os.path.join(dir_executables + "prime.jar"),
}

def execute_program(program, args):
    java = "java -jar".split(" ")
    p = Popen(java + [program] + args, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = p.communicate(input='passed_string')
    return stdout

# @app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


current_milli_time = lambda: int(round(time.time() * 1000))

@app.get("/")
def index():
    return "MobileCloudBenchServer working"

def get_executable_path(name):
    path = os.path.join(app_dir, "executables", name)
    if os.path.exists(path):
        return path
    return None


def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()
        client_time = long(request.query.get('send_time', 0))
        request_time = int(current_milli_time() - client_time)

        ret = fn(*args, **kwargs)

        elapsed_time = int((time.time() - start_time) * 1000)

        response.set_header("request-time", str(request_time))
        response.set_header("compute-time-server", str(elapsed_time))
        return ret

    return with_profiling

@app.get("/linpack")
@profile
def run_linpack():
    parameter = request.query.get('parameter', "")
    executable = get_executable_path("linpackbm.jar")
    out = execute_program(executable, [parameter])

    return out

@app.get("/primecalc")
@profile
def run_primecalc():
    parameter = request.query.get('parameter', "")
    executable = get_executable_path("primebm.jar")
    out = execute_program(executable, [parameter])
    return out

@app.post("/sorttext")
def run_sorttext():
    parameter = request.forms.get('parameter', "")
    executable = get_executable_path("sorttext.jar")
    out = execute_program(executable, [parameter])
    return out


if __name__ == "__main__":
    bottle.debug(True)
    bottle.run(app=app, server="gunicorn", host='localhost', 
        port=5000, workers=4, reload=True, debug=True)