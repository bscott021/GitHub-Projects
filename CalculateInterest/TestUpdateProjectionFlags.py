
import unittest
from unittest.mock import patch, Mock

# import json

from helpers import updateProjectionFlags


class TestUpdateProjectionFlags(unittest.TestCase):

    # Test that valid input gives a successful return value
    @patch('os.getenv', return_value='testToken')
    @patch('requests.put')
    def test_valid_input(self, mock_getenv, mock_put):
        mockResponse = Mock()
        mockResponse.raise_for_status.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"}
        mockResponse.json.return_value = {'status': 'success'}
        mock_put.return_value = mockResponse
    
        returnVal = updateProjectionFlags('GoodColumnIdVal', True, False)
        self.assertTrue(returnVal)
    
    # Test that 1 bad input gives an unsuccessful return value 
    @patch('os.getenv', return_value='testToken')
    def test_1_bad_input(self, mock_getenv):
        returnVal = updateProjectionFlags('GoodColumnIdVal', 'BadRunVal', False)
        self.assertFalse(returnVal)

    # Test that multiple bad inputs gives an unsuccessful return value
    @patch('os.getenv', return_value='testToken')
    def test_multiple_bad_inputs(self, mock_getenv):
        returnVal = updateProjectionFlags(0, 'BadRunVal', False)
        self.assertFalse(returnVal)

    # Test that no auth token gets an unsuccessful return val
    @patch('os.getenv', return_value=None)
    def test_no_auth_token(self, mock_getenv):
        returnVal = updateProjectionFlags('GoodColumnIdVal', True, False)
        self.assertFalse(returnVal)

    # Test successful put request (HTTP 202)
    @patch('os.getenv', return_value='testToken')
    @patch('requests.put')
    def test_202_response(self, mock_getenv, mock_put):
        mockResponse = Mock()
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"}
        mock_put.return_value = mockResponse

        returnVal = updateProjectionFlags('GoodColumnIdVal', True, False)
        self.assertTrue(returnVal)
    
    """
    # Test 400
    @patch('os.getenv', return_value='testToken')
    @patch('requests.put')
    def test_400_response(self, mock_getenv, mock_put):
        mockResponse = Mock()
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"}
        mock_put.return_value = mockResponse

        returnVal = updateProjectionFlags('GoodColumnIdVal', True, False)
        self.assertTrue(returnVal)
    """

if __name__ == '__main__':
    unittest.main()

