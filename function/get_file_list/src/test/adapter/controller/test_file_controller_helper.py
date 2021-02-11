from unittest import TestCase

from lib.adapter.controller.file_controller_helper import FileControllerHelper
from lib.exception.validation_exception import ValidationException


class TestFileControllerHelper(TestCase):
    def test_validate_list_event__ok(self):
        event1 = {
            'date_to': '2020-01-01',
            'date_from': '2020-11-11'
        }
        FileControllerHelper.validate_list_event(event1)

        event2 = {
            'date_to': '2020-01-01',
            'date_from': '2020-11-11',
            'channel': 'channel',
        }
        FileControllerHelper.validate_list_event(event2)

        event3 = {
            'date_to': '2020-01-01',
            'date_from': '2020-11-11',
            'channel': 'channel',
            'user': 'user'
        }
        FileControllerHelper.validate_list_event(event3)

    def test_validate_list_event__raise(self):
        event1 = {
        }
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_list_event(event1)

        event2 = {
            'date_to': '2020-01-01',
        }
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_list_event(event2)

        event3 = {
            'date_from': '2020-11-01',
        }
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_list_event(event3)

        event4 = {
            'date_to': '2020-01-01',
            'date_from': '2020-11-01',
            'channel': ''
        }
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_list_event(event4)

        event5 = {
            'date_to': '2020-01-01',
            'date_from': '2020-11-01',
            'user': ''
        }
        with self.assertRaises(ValidationException):
            FileControllerHelper.validate_list_event(event5)
