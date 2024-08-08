
import unittest
from unittest.mock import patch, Mock
import requests
from helpers import addProjectionRows
from ProjectionRow import ProjectionRow

class TestAddProjectionRows(unittest.TestCase):

    @property
    def configDict(self):
        return {
        'basePath': 'http://test.com',
        'docId': 'doc-id',
        'projectionDataTableId': 'table-id', 
        "projectionTextColId": "col1",
        "numMonthsColId": "col2",
        "numContributorsColId": "col3",
        "individualContributionColId": "col4",
        "totalContributionsColId": "col5",
        "startingBalanceColId2": "col6",
        "currentBalanceColId": "col7",
        "interestGainedColId": "col8"
    }
    
    # Test that no auth token returns False
    @patch('os.getenv', return_value=None)
    def test_no_auth_token(self, mock_getenv):
        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0)])
        self.assertFalse(returnVal)

        # Additional check for good input
        mock_getenv.assert_called_once_with('authToken')


    # Test no config
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_no_config(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = {}

        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0)])
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()


    # Test that valid input returns True 
    @patch('helpers.loadConfig')
    @patch('requests.post')
    @patch('os.getenv', return_value='testToken')
    def test_valid_input(self, mock_getenv, mock_post, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 202
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "addedRowIds": ["i-bCdeFgh","i-CdEfgHi"]}
        mock_post.return_value = mockResponse
            
        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0)])
        self.assertTrue(returnVal)

        # Additional checks for good input
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_post.assert_called_once()
    

    # Test valid with invalid input data. Returns True since it could should still post something
    @patch('helpers.loadConfig')
    @patch('requests.post')
    @patch('os.getenv', return_value='testToken')
    def test_valid_with_invalid_input(self, mock_getenv, mock_post, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 202
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "addedRowIds": ["i-bCdeFgh","i-CdEfgHi"]}
        mock_post.return_value = mockResponse
            
        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0), "NotAProjectionRowObject"])
        self.assertTrue(returnVal)

        # Additional checks for good input
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_post.assert_called_once()
    

    # Test non list value returns False
    def test_empty_input(self):
        returnVal = addProjectionRows(1)
        self.assertFalse(returnVal)


    # Test empty list returns False
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_empty_list_input(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = self.configDict
            
        returnVal = addProjectionRows([])
        self.assertFalse(returnVal)

        # Additional checks patching calls
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()


    # Test unsuccessful call due to multiple bad inputs. Returns False
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_multiple_bad_input(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = self.configDict

        returnVal = addProjectionRows([1, 'SecondInvalidValue'])
        self.assertFalse(returnVal)

        # Additional checks for patching calls
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()


    # Test successful put request (HTTP 202) returns True 
    @patch('helpers.loadConfig')
    @patch('requests.post')
    @patch('os.getenv', return_value='testToken')
    def test_202_response(self, mock_getenv, mock_post, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 202
        mockResponse.raise_for_status.return_value = None
        mockResponse.json.return_value = {"requestId": "abc-123-def-456", "addedRowIds": ["i-bCdeFgh","i-CdEfgHi"]}
        mock_post.return_value = mockResponse

        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0)])
        self.assertTrue(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_post.assert_called_once()
    
    
    # Test Bad HTTP Response (400, 401, 403, 404, 429) returns False
    @patch('helpers.loadConfig')
    @patch('requests.post')
    @patch('os.getenv', return_value='testToken')
    def test_400_response(self, mock_getenv, mock_post, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockResponse = Mock()
        mockResponse.status_code = 400
        mockResponse.raise_for_status.return_value = requests.exceptions.HTTPError(response=Mock(status=400))
        mockResponse.json.return_value = {"statusCode": 400, "statusMessage": "Bad Request", "message": "Bad Request"}
        mock_post.return_value = mockResponse

        returnVal = addProjectionRows([ProjectionRow("Test Id", 1, 1, 100, 100, 0, 100, 0)])
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_post.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()

