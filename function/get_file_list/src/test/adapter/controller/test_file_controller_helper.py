import base64
from datetime import datetime
from typing import Dict
from unittest import TestCase
from urllib.parse import urlencode

import pytz

from lib.adapter.controller.file_controller_helper import FileControllerHelper
from lib.adapter.controller.model.slash_command_body import SlashCommandBody
from lib.exception.validation_exception import ValidationException


class TestFileControllerHelper(TestCase):
    def test_get_command_header(self):
        event: Dict = {
            'headers': {
                'x-slack-request-timestamp': '1577804400',
                'x-slack-signature': 'sig1'
            }
        }

        actual = FileControllerHelper.get_command_header(event)

        self.assertEqual(actual.slack_signature, "sig1")
        self.assertEqual(actual.slack_request_timestamp,
                         datetime.fromtimestamp(1577804400, tz=pytz.timezone('Asia/Tokyo')))

    def test_get_command_body(self):
        body: Dict = {
            'token': 'token1',
            'user_id': 'user_id1',
            'channel_id': 'channel_id1',
            'command': 'command1',
            'text': 'text1',
        }
        encoded_dict = urlencode(body)
        encoded = base64.b64encode(encoded_dict.encode('utf-8'))
        event: Dict = {
            'body': encoded
        }

        actual = FileControllerHelper.get_command_body(event)

        self.assertEqual('token1', actual.token)
        self.assertEqual('user_id1', actual.user_id)
        self.assertEqual('channel_id1', actual.channel_id)
        self.assertEqual('command1', actual.command)
        self.assertEqual('text1', actual.text)

    def test_valid_signature(self):
        event1: Dict = {
            'headers': {
                'x-slack-request-timestamp': '1577804400',
                'x-slack-signature': 'v0=c69bbddee42b0d184be364253e1fa52ae8c5b7886a606aae6abc3c20f9d79c2e'
            },
            'body': base64.b64encode(
                'token=token_1&user_id=user_id1&channel_id=channel_id1&command=command_1&text=text_1'.encode('utf-8'))
        }

        actual1 = FileControllerHelper.valid_signature(event1, 'secret')
        self.assertTrue(actual1)

        event2: Dict = {
            'headers': {
                'x-slack-request-timestamp': '1577804400',
                'x-slack-signature': 'v0=wrong'
            },
            'body': base64.b64encode('token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J'.encode('utf-8'))

        }

        actual2 = FileControllerHelper.valid_signature(event2, 'secret')
        self.assertFalse(actual2)

    def test_parse_text(self):
        text1 = ' from=2020/01/01  to=2020/11/11'
        actual1 = FileControllerHelper.parse_text(text1)
        self.assertEqual('2020/01/01', actual1.date_from)
        self.assertEqual('2020/11/11', actual1.date_to)
        self.assertEqual(actual1.all_users, False)
        self.assertEqual(actual1.all_channels, False)

        text2 = ' from=2020/01/01  to=2020/11/11 -ac -au'
        actual2 = FileControllerHelper.parse_text(text2)
        self.assertEqual('2020/01/01', actual2.date_from)
        self.assertEqual('2020/11/11', actual2.date_to)
        self.assertEqual(actual2.all_users, True)
        self.assertEqual(actual2.all_channels, True)

        text3 = ' from=2020/01/01  to=2020/11/11 --all-channels --all-users'
        actual3 = FileControllerHelper.parse_text(text3)
        self.assertEqual('2020/01/01', actual3.date_from)
        self.assertEqual('2020/11/11', actual3.date_to)
        self.assertEqual(actual3.all_users, True)
        self.assertEqual(actual3.all_channels, True)

    def test_validate_body__ok(self):
        body1 = SlashCommandBody(
            token='token1',
            user_id='user_id1',
            channel_id='channel_id1',
            command='command1',
            text='to=2020/01/01 from=2020/11/11',
        )
        FileControllerHelper.validate_body(body1)

        body2 = SlashCommandBody(
            token='token2',
            user_id='user_id2',
            channel_id='channel_id2',
            command='command2',
            text=' to=2020/01/01   from=2020/11/11',
        )
        FileControllerHelper.validate_body(body2)

        body3 = SlashCommandBody(
            token='token3',
            user_id='user_id3',
            channel_id='channel_id3',
            command='command3',
            text=' to=2020/01/01 from=2020/11/11 -ac -au',
        )
        FileControllerHelper.validate_body(body3)

        body4 = SlashCommandBody(
            token='token4',
            user_id='user_id4',
            channel_id='channel_id4',
            command='command4',
            text=' to=2020/01/01 from=2020/11/11 --all-channels --all-users',
        )
        FileControllerHelper.validate_body(body4)

        body5 = SlashCommandBody(
            token='token5',
            user_id='user_id5',
            channel_id='channel_id5',
            command='command5',
            text=' to=2020/01/01 from=2020/11/11 -ac',
        )
        FileControllerHelper.validate_body(body5)

        body6 = SlashCommandBody(
            token='token6',
            user_id='user_id6',
            channel_id='channel_id6',
            command='command6',
            text=' to=2020/01/01 from=2020/11/11 -au',
        )
        FileControllerHelper.validate_body(body6)

        body7 = SlashCommandBody(
            token='token7',
            user_id='user_id7',
            channel_id='channel_id7',
            command='command7',
            text=' to=2020/01/01 from=2020/11/11 --all-users',
        )
        FileControllerHelper.validate_body(body7)

        body8 = SlashCommandBody(
            token='token8',
            user_id='user_id8',
            channel_id='channel_id8',
            command='command8',
            text=' to=2020/01/01 from=2020/11/11 --all-channels',
        )
        FileControllerHelper.validate_body(body8)

    def test_validate_body__raise(self):
        body1 = SlashCommandBody(
            token='',
            user_id='user_id1',
            channel_id='channel_id1',
            command='command1',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body1)

        body2 = SlashCommandBody(
            token='token2',
            user_id='',
            channel_id='channel_id2',
            command='command2',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body2)

        body3 = SlashCommandBody(
            token='token3',
            user_id='user_id3',
            channel_id='',
            command='command3',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body3)

        body4 = SlashCommandBody(
            token='token4',
            user_id='user_id4',
            channel_id='channel_id4',
            command='',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body4)

        body5 = SlashCommandBody(
            token='token5',
            user_id='user_id5',
            channel_id='channel_id5',
            command='command5',
            text='',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body5)

        body6 = SlashCommandBody(
            token='token6',
            user_id='user_id6',
            channel_id='channel_id6',
            command='command6',
            text='to=2020/01/01 from=xxxx/xx/xx',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body6)

        body7 = SlashCommandBody(
            token='token7',
            user_id='user_id7',
            channel_id='channel_id7',
            command='command7',
            text='to=xxxx/xx/xx from=2020/10/10',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body7)
