import os

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def list(token):
    url = "{}/service/instance".format(host())
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def get(name, token):
    url = "{}/service/instance/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def alarms_by_instance(instance, token):
    url = "{}/alarm/instance/{}".format(host(), instance)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
