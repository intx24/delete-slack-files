import base64
from typing import Dict
from unittest import TestCase, mock
from urllib.parse import urlencode

from lib.adapter.controller.controller_helper import ControllerHelper
from lib.adapter.controller.model.slash_command import SlashCommandHeaders


class TestControllerHelper(TestCase):
    def test_get_command_header(self):
        event: Dict = {
            'headers': {
                'x-slack-request-timestamp': '1577804400',
                'x-slack-signature': 'sig1'
            }
        }

        actual = ControllerHelper.get_command_header(event)

        self.assertEqual(actual.slack_signature, "sig1")
        self.assertEqual(actual.slack_request_timestamp, 1577804400)

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

        actual = ControllerHelper.get_command_body(event)

        self.assertEqual('token1', actual.token)
        self.assertEqual('user_id1', actual.user_id)
        self.assertEqual('channel_id1', actual.channel_id)
        self.assertEqual('command1', actual.command)
        self.assertEqual('text1', actual.text)

    def test_valid_signature(self):
        headers1 = SlashCommandHeaders(
            slack_request_timestamp=1531420618,
            slack_signature='v0=a2114d57b48eac39b9ad189dd8316235a7b4a8d21a10bd27519666489c69b503'
        )
        body1 = 'token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V' \
                '&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text' \
                '=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554' \
                '%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c'

        actual1 = ControllerHelper.valid_signature(headers1, body1, '8f742231b10e8888abcd99yyyzzz85a5')
        self.assertTrue(actual1)

        headers2 = SlashCommandHeaders(
            slack_request_timestamp=1531420618,
            slack_signature='v0=wrong'
        )
        body2 = 'token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V' \
                '&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text' \
                '=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554' \
                '%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c'
        actual2 = ControllerHelper.valid_signature(headers2, body2, '8f742231b10e8888abcd99yyyzzz85a5')
        self.assertFalse(actual2)

    @mock.patch('time.time')
    def test_validate_timestamp(self, mock_time):
        timestamp1 = 1577804700
        mock_time.return_value = 1577804400
        actual = ControllerHelper.valid_timestamp(timestamp1)
        self.assertTrue(actual)

        timestamp1 = 1577804800
        mock_time.return_value = 1577804400
        actual = ControllerHelper.valid_timestamp(timestamp1)
        self.assertFalse(actual)

