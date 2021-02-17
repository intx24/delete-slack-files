from unittest import TestCase

from lib.adapter.controller.file_controller_helper import FileControllerHelper
from lib.adapter.controller.model.slack_command_body import SlackCommandBody
from lib.exception.validation_exception import ValidationException


class TestFileControllerHelper(TestCase):
    def test_validate_body__ok(self):
        body1 = SlackCommandBody(
            token='token1',
            user_id='user_id1',
            channel_id='channel_id1',
            command='command1',
            text='to=2020/01/01 from=2020/11/11',
        )
        FileControllerHelper.validate_body(body1)

        body2 = SlackCommandBody(
            token='token2',
            user_id='user_id2',
            channel_id='channel_id2',
            command='command2',
            text=' to=2020/01/01   from=2020/11/11',
        )
        FileControllerHelper.validate_body(body2)

        body3 = SlackCommandBody(
            token='token3',
            user_id='user_id3',
            channel_id='channel_id3',
            command='command3',
            text=' to=2020/01/01 from=2020/11/11 -ac -au',
        )
        FileControllerHelper.validate_body(body3)

        body4 = SlackCommandBody(
            token='token4',
            user_id='user_id4',
            channel_id='channel_id4',
            command='command4',
            text=' to=2020/01/01 from=2020/11/11 --all-channels --all-users',
        )
        FileControllerHelper.validate_body(body4)

        body5 = SlackCommandBody(
            token='token5',
            user_id='user_id5',
            channel_id='channel_id5',
            command='command5',
            text=' to=2020/01/01 from=2020/11/11 -ac',
        )
        FileControllerHelper.validate_body(body5)

        body6 = SlackCommandBody(
            token='token6',
            user_id='user_id6',
            channel_id='channel_id6',
            command='command6',
            text=' to=2020/01/01 from=2020/11/11 -au',
        )
        FileControllerHelper.validate_body(body6)

        body7 = SlackCommandBody(
            token='token7',
            user_id='user_id7',
            channel_id='channel_id7',
            command='command7',
            text=' to=2020/01/01 from=2020/11/11 --all-users',
        )
        FileControllerHelper.validate_body(body7)

        body8 = SlackCommandBody(
            token='token8',
            user_id='user_id8',
            channel_id='channel_id8',
            command='command8',
            text=' to=2020/01/01 from=2020/11/11 --all-channels',
        )
        FileControllerHelper.validate_body(body8)

    def test_validate_body__raise(self):
        body1 = SlackCommandBody(
            token='',
            user_id='user_id1',
            channel_id='channel_id1',
            command='command1',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body1)

        body2 = SlackCommandBody(
            token='token2',
            user_id='',
            channel_id='channel_id2',
            command='command2',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body2)

        body3 = SlackCommandBody(
            token='token3',
            user_id='user_id3',
            channel_id='',
            command='command3',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body3)

        body4 = SlackCommandBody(
            token='token4',
            user_id='user_id4',
            channel_id='channel_id4',
            command='',
            text='to=2020/01/01 from=2020/11/11',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body4)

        body5 = SlackCommandBody(
            token='token5',
            user_id='user_id5',
            channel_id='channel_id5',
            command='command5',
            text='',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body5)

        body6 = SlackCommandBody(
            token='token6',
            user_id='user_id6',
            channel_id='channel_id6',
            command='command6',
            text='to=2020/01/01 from=xxxx/xx/xx',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body6)

        body7 = SlackCommandBody(
            token='token7',
            user_id='user_id7',
            channel_id='channel_id7',
            command='command7',
            text='to=xxxx/xx/xx from=2020/10/10',
        )
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_body(body7)
