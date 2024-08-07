
import unittest
from unittest.mock import patch, Mock
import requests
from helpers import deleteProjectionRows
from Classes.ProjectionRow import ProjectionRow

class TestDeleteProjectionRows(unittest.TestCase):

    @property
    def configDict(self):
        return {
        'basePath': 'http://test.com',
        'docId': 'doc-id',
        "projectionDataTableId": "grid-id",
        "projectionTextColId": "c-1"
    }

    # Test Bad Input Type
    def test_bad_input_type(self):
        returnVal = deleteProjectionRows(1)
        self.assertFalse(returnVal)


    # Test Empty Input Empty String
    def test_empty_str_input(self):
        returnVal = deleteProjectionRows('')
        self.assertFalse(returnVal)
    
    
    # Test that no auth token returns False
    @patch('os.getenv', return_value=None)
    def test_no_auth_token(self, mock_getenv):
        returnVal = deleteProjectionRows('Test Text')
        self.assertFalse(returnVal)

        # Additional check for good input
        mock_getenv.assert_called_once_with('authToken')
    
    
    # Test no config
    @patch('helpers.loadConfig')
    @patch('os.getenv', return_value='testToken')
    def test_no_config(self, mock_getenv, mock_load_config):
        mock_load_config.return_value = {}

        returnVal = deleteProjectionRows('Test Text')
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()

    # Test successful call
    @patch('helpers.loadConfig')
    @patch('requests.delete')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_good_call(self, mock_getenv, mock_get, mock_delete, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockGetResponse = Mock()
        mockGetResponse.status_code = 200
        mockGetResponse.raise_for_status.return_value = None
        mockGetResponse.json.return_value = {"items": [{"id": "i-grZ1jP5Uk3","values": {"c-1": '1', "c-2": '2', "c-3": '3', "c-4": '4', "c-5": '5',"c-6": '6',"c-7": '7',"c-8": '8',"c-9": 'Val',"c-10": 'Val', "c-11": 'Val', "c-12": 'Val'}}]}
        mock_get.return_value = mockGetResponse

        mockDeleteResponse = Mock()
        mockDeleteResponse.status_code = 202
        mockDeleteResponse.raise_for_status.return_value = None
        mockDeleteResponse.json.return_value = {"requestId": "abc-123-def-456", "id": "i-tuVwxYz"}
        mock_delete.return_value = mockDeleteResponse

        returnVal = deleteProjectionRows('Test Text')
        self.assertTrue(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()
        mock_delete.assert_called_once()
    

    # Test Get returns nothing for items. Expecting True for success because there was nothing to delete
    @patch('helpers.loadConfig')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_get_no_data(self, mock_getenv, mock_get, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockGetResponse = Mock()
        mockGetResponse.status_code = 200
        mockGetResponse.raise_for_status.return_value = None
        mockGetResponse.json.return_value = {"items": [], "href": "https://test.com"}
        mock_get.return_value = mockGetResponse

        returnVal = deleteProjectionRows('Test Text')
        self.assertTrue(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()

    
    # Test unsuccessful Get call returns False 
    @patch('helpers.loadConfig')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_get_404_response(self, mock_getenv, mock_get, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockGetResponse = Mock()
        mockGetResponse.status_code = 404
        mockGetResponse.raise_for_status.return_value = requests.exceptions.HTTPError(response=Mock(status=404))
        mockGetResponse.json.return_value = {"statusCode": 404, "statusMessage": "Not Found", "message": "Not Found"}
        mock_get.return_value = mockGetResponse

        returnVal = deleteProjectionRows('Test Text')
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()


    # Test Unsuccessful Delete - False 
    @patch('helpers.loadConfig')
    @patch('requests.delete')
    @patch('requests.get')
    @patch('os.getenv', return_value='testToken')
    def test_404_delete_response(self, mock_getenv, mock_get, mock_delete, mock_load_config):
        mock_load_config.return_value = self.configDict

        mockGetResponse = Mock()
        mockGetResponse.status_code = 200
        mockGetResponse.raise_for_status.return_value = None
        mockGetResponse.json.return_value = {"items": [{"id": "i-grZ1jP5Uk3","values": {"c-1": '1', "c-2": '2', "c-3": '3', "c-4": '4', "c-5": '5',"c-6": '6',"c-7": '7',"c-8": '8',"c-9": 'Val',"c-10": 'Val', "c-11": 'Val', "c-12": 'Val'}}]}
        mock_get.return_value = mockGetResponse

        mockDeleteResponse = Mock()
        mockDeleteResponse.status_code = 404
        mockDeleteResponse.raise_for_status.return_value = requests.exceptions.HTTPError(response=Mock(status=404))
        mockDeleteResponse.json.return_value = {"statusCode": 404, "statusMessage": "Not Found", "message": "Not Found"}
        mock_delete.return_value = mockDeleteResponse

        returnVal = deleteProjectionRows('Test Text')
        self.assertFalse(returnVal)

        # Additional checks for patch calls 
        mock_getenv.assert_called_once_with('authToken')
        mock_load_config.assert_called_once()
        mock_get.assert_called_once()
        mock_delete.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()

