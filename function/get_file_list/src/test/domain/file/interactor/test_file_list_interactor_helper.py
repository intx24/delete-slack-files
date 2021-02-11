from unittest import TestCase

from lib.domain.file.interactor.file_list_interactor_helper import FileListInteractorHelper
from lib.domain.file.model.get_files_list_params import GetFilesListParams
from lib.exception.validation_exception import ValidationException
from lib.usecase.file.list.file_list_input import FileListInput


class TestFileListInteractorHelper(TestCase):
    def test_convert(self):
        input_data: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            channel='channel',
            user='user'
        )

        actual = FileListInteractorHelper.convert(input_data)
        expected = GetFilesListParams(
            token='token',
            channel='channel',
            ts_from=1577804400,
            ts_to=1605020400,
            user='user'
        )
        self.assertEqual(expected, actual)

    def test_valid_input__ok(self):
        input_data1: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11'
        )
        FileListInteractorHelper.validate_input(input_data1)

        input_data2: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            user='user1'
        )
        FileListInteractorHelper.validate_input(input_data2)

        input_data3: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            channel='channel1'
        )
        FileListInteractorHelper.validate_input(input_data3)

        input_data4: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            channel='channel1',
            user='user1'
        )
        FileListInteractorHelper.validate_input(input_data4)

    def test_valid_input__raise(self):
        input_data1: FileListInput = FileListInput(
            token='',
            date_from='2020-01-01',
            date_to='2020-11-11'
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data1)

        input_data2: FileListInput = FileListInput(
            token='token',
            date_from='',
            date_to='2020-11-11'
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data2)

        input_data3: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to=''
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data3)

        input_data4: FileListInput = FileListInput(
            token='token',
            date_from='date_from',
            date_to='2020-11-11'
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data4)

        input_data5: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='date_to'
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data5)

        input_data6: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            user='',
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data6)

        input_data7: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11',
            channel='',
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_input(input_data7)

    def test_valid_param__ok(self):
        param1: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
        )
        FileListInteractorHelper.validate_param(param1)

        param2: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            user='user1'
        )
        FileListInteractorHelper.validate_param(param2)

        param3: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            channel='channel1'
        )
        FileListInteractorHelper.validate_param(param3)

        param4: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            user='user1',
            channel='channel1'
        )
        FileListInteractorHelper.validate_param(param4)

    def test_valid_param__raise(self):
        param1: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            user=''
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_param(param1)

        param2: GetFilesListParams = GetFilesListParams(
            token='token',
            ts_from=1577804400,
            ts_to=1605020400,
            channel=''
        )
        with self.assertRaises(ValidationException):
            FileListInteractorHelper.validate_param(param2)
