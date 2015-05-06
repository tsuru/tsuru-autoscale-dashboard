import os

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def list():
    url = "{}/action".format(host())
    response = requests.get(url)
    return response
