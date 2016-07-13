import os
import requests
import bottle
from bottle import Bottle, redirect, route
from bottle import template, SimpleTemplate
from bottle import get, post, request, response
from urlparse import urlparse
from subprocess import Popen, PIPE, STDOUT

app = Bottle()

app_dir = os.path.dirname(os.path.abspath(__file__))

dir_executables = os.path.join(app_dir, "executables", name)

BENCHMARKS = {
    "linpack": dir_executables + "linpackbm.jar",
    "prime": dir_executables + "prime.jar",
    "image": dir_executables + "prime.jar",
}

def execute_program(program, args):
    java = "java -jar".split(" ")
    p = Popen(java + [program] + args, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = p.communicate(input='passed_string')
    return stdout

@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
    print(request.environ['PATH_INFO'])

def get_executable_path(name):
    path = os.path.join(app_dir, "executables", name)
    if os.path.exists(path):
        return path
    return None

@app.get("/linpack")
def run_linpack():
    parameter = request.query.get('parameter', "")
    executable = get_executable_path("linpackbm.jar")
    out = execute_program(executable, [parameter])
    return out

@app.post("/sorttext")
def run_sorttext():
    parameter = request.forms.get('parameter', "")
    executable = get_executable_path("sorttext.jar")
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
    bottle.run(app=app, host='localhost', port=5000, workers=4)