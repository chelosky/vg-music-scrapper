import requests

def request(method, url, **kwargs):
    session = requests.Session()

    return getattr(session, method)(url, verify=False, **kwargs)
