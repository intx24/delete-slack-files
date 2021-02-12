#!/usr/bin/env python3
from typing import List

import requests

from lib.domain.file.model.file import File
from lib.domain.file.model.get_files_list_params import GetFilesListParams
from lib.domain.file.repository.abstract_file_repository import AbstractFileRepository
from lib.exception.external_api_call_exception import ExternalApiCallException


class SlackDriver(AbstractFileRepository):
    endpoint = 'https://slack.com/api/files.list'

    def get_files_list(self, params: GetFilesListParams) -> List[File]:
        url = self.endpoint
        url += f'?token={params.token}'

        if params.ts_from:
            url += f'&ts_from={params.ts_from}'
        if params.ts_to:
            url += f'&ts_to={params.ts_to}'
        if params.channel:
            url += f'&channel={params.channel}'
        if params.user:
            url += f'&user={params.user}'

        res = requests.get(url)
        res_json = res.json()
        print(res_json)

        if res_json['ok'] is False:
            raise ExternalApiCallException('calling files.list was failed. reason: ' + res_json['error'])

        files: List[File] = []
        for v in res_json['files']:
            file = File(
                id=v['id'],
                created=v['created'],
                timestamp=v['timestamp'],
                name=v['name'],
                title=v['title'],
                filetype=v['filetype'],
                mimetype=v['mimetype'],
                user=v['user'],
                size=v['size'],
                is_public=v['is_public'],
                username=v['username'],
                url_private=v['url_private'],
                url_private_download=v['url_private_download']
            )
            files.append(file)

        return files
