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