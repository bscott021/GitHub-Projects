
import unittest
from unittest.mock import patch, Mock
import requests
from helpers import getProjectionQueue
from Classes.ProjectionRow import ProjectionRow

class TestGetProjectionQueue(unittest.TestCase):

    @property
    def configDict(self):
        return {
        'basePath': 'http://test.com',
        'docId': 'doc-id',
        "projectionHeaderTableId": "grid-id",
        "runColId": "c-1",
        "generatedColId": "c-2",
        "projetionColId": "c-3",
        "totalMonthsColId": "c-4",
        "contributorsColId": "c-5",
        "individualAmountColId": "c-6",
        "increaseAmountColId": "c-7",
        "monthsToIncreaseColId": "c-8",
        "startingBalanceColId": "c-9",
        "yearlyInterestRateColId": "c-10"
    }
    
    # Test that no auth token returns False
    @patch('os.getenv', return_value=None)
    def test_no_auth_token(self, mock_getenv):
        returnVal = getProjectionQueue()
        self.assertFalse(returnVal)

        # Additional checks for good input
        mock_getenv.assert_called_once_with('authToken')
    

    # Test no config
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_no_config(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = {}

        returnVal = getProjectionQueue()
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()


    # Test successful put request (HTTP 202) but there was nothing to process so this expects False 
    @patch('helpers.loadConfig')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_202_with_response_data(self, mock_getenv, mock_get, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 200
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"items": [{"id": "i-grZ1jP5Uk3","values": {"c-1": False, "c-2": True, "c-3": 'Test', "c-4": '1', "c-5": '1',"c-6": '100',"c-7": '50',"c-8": '1',"c-9": '0',"c-10": '0.05'}}]}
        mock_get.return_value = mockResponse

        returnVal = getProjectionQueue()
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()
    

    # Test successful put request (HTTP 202) returns True 
    @patch('helpers.loadConfig')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_202_with_no_response_data(self, mock_getenv, mock_get, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 200
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"items": [{"id": "i-grZ1jP5Uk3","values": {"c-1": "Name","c-2": '1',"c-3": '1',"c-4": '100',"c-5": '50',"c-6": '1',"c-7": '0',"c-8": '0.05',"c-9": 'false',"c-10": 'true'}}]}
        mock_get.return_value = mockResponse

        returnVal = getProjectionQueue()
        self.assertIsInstance(returnVal, list)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()

    
    # Test Bad HTTP Response (401, 403, 404, 429) returns False
    @patch('helpers.loadConfig')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_404_response(self, mock_getenv, mock_get, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 404
        mockResponse.raise_for_status.return_value = requests.exceptions.HTTPError(response=Mock(status=404))
        mockResponse.json.return_value = {"statusCode": 404, "statusMessage": "Not Found", "message": "Not Found"}
        mock_get.return_value = mockResponse

        returnVal = getProjectionQueue()
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()

