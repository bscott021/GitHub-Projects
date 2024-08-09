
import unittest
from unittest.mock import patch, Mock
import requests
from helpers import updateProjectionFlags


class TestUpdateProjectionFlags(unittest.TestCase):

    @property
    def configDict(self):
        return {
            'basePath': 'http://test.com',
            'docId': 'doc-id',
            'projectionHeaderTableId': 'table-id',
            'runColId': 'run-col-id',
            'generatedColId': 'run-col-id'
    }
    
    
    # Test that valid input gives a successful return value
    @patch('helpers.loadConfig')
    @patch('requests.put')
    @patch('os.getenv', return_value='testToken')
    def test_valid_input(self, mock_getenv, mock_put, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 202
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"} # {'status': 'success'}
        mock_put.return_value = mockResponse
    
        returnVal = updateProjectionFlags('GoodRowIdVal', True, False)
        self.assertTrue(returnVal)

        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_put.assert_called_once()
    

    # Test that 1 bad input gives an unsuccessful return value 
    def test_1_bad_input(self):
        returnVal = updateProjectionFlags('GoodRowIdVal', 'BadRunVal', False)
        self.assertFalse(returnVal)


    # Test that multiple bad inputs gives an unsuccessful return value
    def test_multiple_bad_inputs(self):
        returnVal = updateProjectionFlags(0, 'BadRunVal', False)
        self.assertFalse(returnVal)


    # Test that no auth token gets an unsuccessful return val
    @patch('os.getenv', return_value=None)
    def test_no_auth_token(self, mock_getenv):
        returnVal = updateProjectionFlags('GoodRowIdVal', True, False)
        self.assertFalse(returnVal)
        mock_getenv.assert_called_once_with('authToken')
    

    # Test no config
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_no_config(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = {}

        returnVal = updateProjectionFlags('GoodRowIdVal', True, False)
        self.assertFalse

        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()

    
    # Test successful put request (HTTP 202)
    @patch('helpers.loadConfig')
    @patch('requests.put')
    @patch('os.getenv', return_value='testToken')
    def test_202_response(self, mock_getenv, mock_put, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 202
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"} # {'status': 'success'}
        mock_put.return_value = mockResponse

        returnVal = updateProjectionFlags('GoodRowIdVal', True, False)
        self.assertTrue(returnVal)

        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_put.assert_called_once()
    
    
    # Test Bad HTTP Response (400, 401, 403, 404, 429)
    @patch('helpers.loadConfig')
    @patch('requests.put')
    @patch('os.getenv', return_value='testToken')
    def test_400_response(self, mock_getenv, mock_put, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 400
        mockResponse.raise_for_status.return_value = requests.exceptions.HTTPError(response=Mock(status=400))
        mockResponse.json.return_value = {"statusCode": 400, "statusMessage": "Bad Request", "message": "Bad Request"}
        mock_put.return_value = mockResponse

        returnVal = updateProjectionFlags('GoodColumnIdVal', True, False)
        self.assertFalse(returnVal)

        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_put.assert_called_once()


if __name__ == '__main__':
    unittest.main()

