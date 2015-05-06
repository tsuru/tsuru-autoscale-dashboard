import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data):
    url = "{}/datasource".format(host())
    response = requests.post(url, data=json.dumps(data))
    return response


def list():
    url = "{}/datasource".format(host())
    response = requests.get(url)
    return response
