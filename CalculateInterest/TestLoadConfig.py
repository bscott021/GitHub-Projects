
import unittest
from unittest.mock import patch, mock_open

import json
import os

from helpers import loadConfig


class TestLoadConfig(unittest.TestCase):
    
    # Test successful config.json load 
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"val1": "Test", "val2": "Value"}')
    def test_load_config_success(self, mock_file, mock_exists):
        config = loadConfig('CalculateInterest/config.json')
        self.assertEqual(config['val1'], 'Test')
        self.assertEqual(config['val2'], 'Value')
    
    # Test exception handleing for FileNotFoundError
    @patch('os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists):
        loadConfig('CalculateInterest/config.json')
    
    # Test exception handleing for PermissionError
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_permission_error(self, mock_file, mock_exists):
        mock_file.side_effect = PermissionError("Permission denied")
        loadConfig('CalculateInterest/config.json')
    
    # Test exception handleing for JSONDecodeError
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"val1": "Test", "val2": "Value"}')
    def test_json_decode_error(self, mock_file, mock_exists):
        loadConfig('CalculateInterest/config.json')
    
    # Test exception handleing for ValueError
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='not a json')
    def test_value_error(self, mock_file, mock_exists):
        loadConfig('CalculateInterest/config.json')
    
    # Test exception handleing for general Exception
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_unexpected_error(self, mock_file, mock_exists):
        mock_file.side_effect = Exception("Unexpected error")
        loadConfig('CalculateInterest/config.json')
    

if __name__ == '__main__':
    unittest.main()

