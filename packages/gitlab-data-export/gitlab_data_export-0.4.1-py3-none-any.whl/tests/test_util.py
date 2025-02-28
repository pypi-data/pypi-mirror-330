import unittest
from unittest.mock import patch

import os
from datetime import datetime

from gitlab_data_export.util import ExportOptions, Result


class TestResult(unittest.TestCase):
    def test_success(self):
        result = Result.success()
        self.assertTrue(result.successful)

    def test_failure(self):
        result = Result.failure()
        self.assertFalse(result.successful)

    def test_bind(self):
        successful_result = Result.success()
        failed_result = Result.failure()

        failed_result.bind(successful_result)
        self.assertFalse(failed_result.successful)

        successful_result.bind(failed_result)
        self.assertFalse(successful_result.successful)

    @patch('sys.exit')
    @patch('logging.error')
    def test_ensure(self, mock_error, mock_exit):
        result = Result.success()
        result.ensure()
        mock_error.assert_not_called()
        mock_exit.assert_not_called()

        result = Result.failure()
        result.ensure()
        mock_error.assert_called_once()
        mock_exit.assert_called_once_with(255)


class TestExportOptions(unittest.TestCase):
    def test_backfill_disabled(self):
        options = ExportOptions('now', True)
        self.assertTrue(options.backfill_disabled)

        options = ExportOptions('2022-01-01 00:00:00', False)
        self.assertFalse(options.backfill_disabled)

    def test_backfill_timestamp(self):
        now = datetime.now()

        options = ExportOptions('now', True)
        self.assertEqual(options.backfill_timestamp(now), now)

        options = ExportOptions('2022-01-01 00:00:00', False)
        self.assertEqual(options.backfill_timestamp(now),
                         datetime(2022, 1, 1, 0, 0))

    @patch.dict(os.environ, {'GITLAB_NO_RECURSION': ''})
    def test_from_env(self):
        with patch.object(os, 'getenv', return_value='2023-01-01 00:00:00'):
            options = ExportOptions.from_env()
            self.assertEqual(options.backfill_time, '2023-01-01 00:00:00')
            self.assertFalse(options.recursion_enabled)

        with patch.object(os, 'getenv', return_value='now'):
            del os.environ['GITLAB_NO_RECURSION']
            options = ExportOptions.from_env()
            self.assertEqual(options.backfill_time, 'now')
            self.assertTrue(options.backfill_disabled)
            self.assertTrue(options.recursion_enabled)
