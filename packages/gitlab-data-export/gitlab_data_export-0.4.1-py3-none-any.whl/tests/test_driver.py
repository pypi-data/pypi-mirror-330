import os
import unittest
from unittest.mock import patch

from gitlab_data_export.driver import get_datastore_factory, BigQuery


class TestBuildDatastore(unittest.TestCase):
    def test_default_datastore_factory_should_be_bigquery(self):
        """Test that a BigQuery object is returned when environment is not set"""
        datastore = get_datastore_factory()
        self.assertEqual(datastore, BigQuery)

    @patch.dict(os.environ, {'GDE_DATASTORE': 'bigquery'})
    def test_bigquery_datastore_factory(self):
        """Test that a BigQuery object is returned when environment is set to bigquery"""
        datastore = get_datastore_factory()
        self.assertEqual(datastore, BigQuery)

    @patch.dict(os.environ, {'GDE_DATASTORE': 'unknown'})
    def test_unknown_datastore_factory(self):
        """Test that an error is raised when an unknown datastore is configured"""
        with self.assertRaises(ValueError):
            get_datastore_factory()
