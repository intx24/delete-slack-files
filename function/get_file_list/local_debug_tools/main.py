#!/usr/bin/env python3
import json

import requests

PORT: int = 8081
URL: str = f'http://localhost:{PORT}/2015-03-31/functions/function/invocations'


def call(url, body):
    print(body)
    res = requests.post(
        url,
        body,
        headers={'Content-Type': 'application/json'})
    print(res.json())


def construct_req_body():
    return json.dumps({
        'date_from': '2020-10-10',
        'date_to': '2021-10-10'
    }).encode('utf-8')


if __name__ == '__main__':
    body: object = construct_req_body()
    call(url=URL, body=body)
