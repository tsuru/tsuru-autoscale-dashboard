import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data):
    url = "{}/alarm".format(host())
    response = requests.post(url, data=json.dumps(data))
    return response
