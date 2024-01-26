import os
import json

import requests

def request(method, url, **kwargs):
    session = requests.Session()

    return getattr(session, method)(url, verify=False, **kwargs)

def download_file(url: str, file_path: str):
    response = request('get', url, stream=True)
    length = response.headers.get('content-length')
    with open(file_path, "wb") as f:
        if length is None:
            f.write(response.content)
        for chunk in response.iter_content(2048):
            f.write(chunk)

def read_json_file(file_path: str) -> dict[str, any] | None:
    if (os.path.isfile(file_path)):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


def create_json_file(data: dict[str, any], file_path: str):
    create_folder(os.path.dirname(file_path))
    with open(file_path, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

def create_folder(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)
