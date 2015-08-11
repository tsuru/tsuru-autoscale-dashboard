import os
import json

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def new(data, token):
    url = "{}/wizard".format(host())
    headers = {"Authorization": token}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response
