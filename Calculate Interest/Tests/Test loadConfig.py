
import unittest
from unittest.mock import patch, mock_open

import json
import os

from helpers import loadConfig


class TestLoadConfig(unittest.TestCase):
    """
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"auth_token": "test_token", "api_key": "test_key"}')
    def test_load_config_success(self, mock_file, mock_exists):
        config = loadConfig('Calculate Interest/config.json')
        self.assertEqual(config['auth_token'], 'test_token')
        self.assertEqual(config['api_key'], 'test_key')
    """
    """
    @patch('os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            loadConfig('Calculate Interest/config.json')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_permission_error(self, mock_file, mock_exists):
        mock_file.side_effect = PermissionError("Permission denied")
        with self.assertRaises(PermissionError):
            loadConfig('Calculate Interest/config.json')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"auth_token": "test_token", "api_key": test_key}')
    def test_json_decode_error(self, mock_file, mock_exists):
        with self.assertRaises(json.JSONDecodeError):
            loadConfig('Calculate Interest/config.json')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='not a json')
    def test_value_error(self, mock_file, mock_exists):
        with self.assertRaises(ValueError):
            loadConfig('Calculate Interest/config.json')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_unexpected_error(self, mock_file, mock_exists):
        mock_file.side_effect = Exception("Unexpected error")
        with self.assertRaises(Exception):
            loadConfig('Calculate Interest/config.json')
    """

if __name__ == '__main__':
    unittest.main()

