
import unittest
from unittest.mock import patch, mock_open

# import json
# import os

from helpers import loadConfig


class TestLoadConfig(unittest.TestCase):
    
    # Test successful config.json load 
    @patch('builtins.open', new_callable=mock_open, read_data='{"val1": "Test", "val2": "Value"}')
    def test_load_config_success(self, mock_file):
        config = loadConfig('CalculateInterest/config.json')
        self.assertEqual(config['val1'], 'Test')
        self.assertEqual(config['val2'], 'Value')
        mock_file.assert_called_once()
    

    # Test exception handleing for FileNotFoundError
    @patch('builtins.open', side_effect=FileNotFoundError, read_data='{"Val1": "Test", "Val2": "Value"}')
    def test_file_not_found(self, mock_file):
        config = loadConfig('CalculateInterest/config.json')
        self.assertIsNone(config)
        mock_file.assert_called_once()


    # Test exception handleing for PermissionError
    @patch('builtins.open', side_effect=FileNotFoundError, read_data='{"Val1": "Test", "Val2": "Value"}')
    def test_permission_error(self, mock_file):
        config = loadConfig('CalculateInterest/config.json')
        self.assertIsNone(config)
        mock_file.assert_called_once()


    # Test exception handleing for JSONDecodeError
    @patch('builtins.open', new_callable=mock_open, read_data='{"Not valid json"}')
    def test_json_decode_error(self, mock_file):
        config = loadConfig('CalculateInterest/config.json')
        self.assertIsNone(config)
        mock_file.assert_called_once()
    

    # Test exception handleing for TypeError
    @patch('builtins.open', new_callable=mock_open, read_data='{"Val1": "Test", "Val2": "Value"}')
    @patch('json.load', side_effect=TypeError)
    def test_value_error(self, mock_json_load, mock_file):
        config = loadConfig('CalculateInterest/config.json')
        self.assertIsNone(config)
        mock_json_load.assert_called_once()
        mock_file.assert_called_once()
    
    
    # Test exception handleing for general Exception
    @patch('builtins.open', new_callable=mock_open)
    def test_unexpected_error(self, mock_file):
        mock_file.side_effect = Exception("Unexpected error")
        config = loadConfig('CalculateInterest/config.json')
        self.assertIsNone(config)
        mock_file.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()

