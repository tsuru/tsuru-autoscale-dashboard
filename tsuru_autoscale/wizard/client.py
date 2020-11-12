import os
import json
import urllib

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def tsuru_host():
    return os.environ.get("TSURU_HOST", "")


def clean_token(token):
    if token.lower().startswith("bearer "):
        return token
    token = urllib.unquote(token)
    token = "bearer {}".format(token)
    return token


def app_info(name, token):
    url = "{}/apps/{}".format(tsuru_host(), name)
    headers = {"Authorization": clean_token(token)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def pool_info(name, token):
    url = "{}/pools/{}".format(tsuru_host(), name)
    headers = {"Authorization": clean_token(token)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def process_list(instance_name, token):
    app = app_info(instance_name, token)
    process = set()

    for u in app.get('units', []):
        process.add(u['ProcessName'])

    p_list = []
    for u in list(process):
        p_list.append((u, u))

    return p_list


def new(data, token):
    url = "{}/wizard".format(host())
    headers = {"Authorization": token}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def get(name, token):
    url = "{}/wizard/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response


def remove(name, token):
    url = "{}/wizard/{}".format(host(), name)
    headers = {"Authorization": token}
    response = requests.delete(url, headers=headers)
    return response


def enable(name, token):
    url = "{}/wizard/{}/enable".format(host(), name)
    headers = {"Authorization": token}
    response = requests.post(url, headers=headers)
    return response


def disable(name, token):
    url = "{}/wizard/{}/disable".format(host(), name)
    headers = {"Authorization": token}
    response = requests.post(url, headers=headers)
    return response


def events(name, token):
    url = "{}/wizard/{}/events".format(host(), name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response
