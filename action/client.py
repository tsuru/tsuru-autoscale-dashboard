import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data):
    url = "{}/action".format(host())
    response = requests.post(url, data=json.dumps(data))
    return response


def list():
    url = "{}/action".format(host())
    response = requests.get(url)
    return response


def remove(name):
    url = "{}/action/{}".format(host(), name)
    response = requests.delete(url)
    return response


def get(name):
    url = "{}/action/{}".format(host(), name)
    response = requests.get(url)
    return response
