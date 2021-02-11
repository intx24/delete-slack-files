from unittest import TestCase

from lib.usecase.file.list.file_list_input import FileListInput


class TestFileListInput(TestCase):
    def test_ts_from(self):
        input_data: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11'
        )
        self.assertEqual(1577804400, input_data.ts_from())

    def test_ts_to(self):
        input_data: FileListInput = FileListInput(
            token='token',
            date_from='2020-01-01',
            date_to='2020-11-11'
        )
        self.assertEqual(1605020400, input_data.ts_to())
