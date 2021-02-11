#!/usr/bin/env python3
import unittest
from unittest import mock

from lib.domain.file.model.file import File
from lib.domain.file.model.get_files_list_params import GetFilesListParams
from lib.driver.api.slack_driver import SlackDriver


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestSlackDriver(unittest.TestCase):
    def setUp(self):
        self.driver = SlackDriver()

    @mock.patch('requests.get')
    def test_get_files_list(self, mock_get):
        res: MockResponse = MockResponse({
            'ok': True,
            'files': [{
                'id': 'id1',
                'created': 1612611194,
                'timestamp': 1612611194,
                'name': 'IMG_1.jpg',
                'title': 'IMG_1.jpg',
                'mimetype': 'image/jpeg',
                'filetype': 'jpg',
                'user': 'user1',
                'size': 1,
                'is_public': False,
                'username': '',
                'url_private': 'url_private1',
                'url_private_download': 'url_private_download1'
            }]
        }, 200)

        mock_get.return_value = res

        actual = self.driver.get_files_list(GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            channel='channel',
            user='user'
        ))
        self.assertEqual(1, len(actual))

        expected = [File(
            id='id1',
            created=1612611194,
            timestamp=1612611194,
            name='IMG_1.jpg',
            title='IMG_1.jpg',
            mimetype='image/jpeg',
            filetype='jpg',
            user='user1',
            size=1,
            is_public=False,
            username='',
            url_private='url_private1',
            url_private_download='url_private_download1')
        ]
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
