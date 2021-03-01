#!/usr/bin/env python3

import json
from base64 import b64encode
from typing import Dict
from urllib.parse import urlencode

import requests

PORT: int = 8082
URL: str = f'http://localhost:{PORT}/2015-03-31/functions/function/invocations'


def call(url, body):
    res = requests.post(
        url,
        body,
        headers={'Content-Type': 'application/json'})
    print(res.json())


def construct_req_body():
    body: Dict = {
        'token': 'token1',
        'user_id': 'user_id1',
        'channel_id': 'channel_id1',
        'command': 'command1',
        'text': 'from=2020/01/01 to=2020/11/11',
    }
    encoded_dict = urlencode(body)
    encoded = b64encode(encoded_dict.encode('utf-8')).decode('utf-8')
    print(encoded)
    return json.dumps({
        'body': encoded
    }).encode('utf-8')


if __name__ == '__main__':
    body: object = construct_req_body()
    print(body)
    call(url=URL, body=body)
