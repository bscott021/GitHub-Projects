
import unittest
from unittest.mock import patch

from helpers import runProjection


class TestUpdateProjectionFlags(unittest.TestCase):
    
    # Test base success case 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_valid_input(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 2)
        self.assertEqual(returnedProjectionRow.totalContributions, 1)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 1.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()


    # Test for when addProjectionRows returns a bad value 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_bad_addProjectionRows_result(self, mock_update, mock_add):

        mock_update.return_value = False
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)
        self.assertTrue(len(returnVal) == 0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()


    # Test for when updateProjectionRows returns a bad value 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_bad_updateProjectionFlags_result(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = False
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)
        self.assertTrue(len(returnVal) == 0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()
    

    # Test for when addProjectionRows and updateProjectionRows return bad values 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_2_bad_def_result(self, mock_update, mock_add):

        mock_update.return_value = False
        mock_add.return_value = False
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)
        self.assertTrue(len(returnVal) == 0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()
    

    # Test 0's 
    def test_zeros(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 0, 0, 0, 0, 0, 0, 0)
        
        self.assertTrue(type(returnVal) == list)
        self.assertEqual(returnVal, [])
    

    # Test 0's with a positiver number of months 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_zeros_with_positive_months(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 0, 0, 0, 0, 0, 0)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1)
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 0)
        self.assertEqual(returnedProjectionRow.individualContribution, 0)
        self.assertEqual(returnedProjectionRow.totalContributions, 0)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 0.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()


    # Test increasing contributors 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_increase_contributors(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 2, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 2)
        self.assertEqual(returnedProjectionRow.individualContribution, 2)
        self.assertEqual(returnedProjectionRow.totalContributions, 2)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 2.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    


    # Test increasing the individual contribution amount
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_increase_contribution_amount(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 2, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 3)
        self.assertEqual(returnedProjectionRow.totalContributions, 2)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 2.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    


    # Test different increase amount 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_different_increase_amount(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 2, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 3)
        self.assertEqual(returnedProjectionRow.totalContributions, 1)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 1.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    
    

    # Test increasing the nuber of months before the contribution is icreased 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_contribution_interval(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 2, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 1)
        self.assertEqual(returnedProjectionRow.totalContributions, 1)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 1.0)
        self.assertEqual(returnedProjectionRow.interestGained, 0.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    
    

    # Test non 0 starting balance 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_valid_input(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 1, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 2)
        self.assertEqual(returnedProjectionRow.totalContributions, 2)
        self.assertEqual(returnedProjectionRow.startingBalance, 1)
        self.assertEqual(returnedProjectionRow.currentBalance, 3.0)
        self.assertEqual(returnedProjectionRow.interestGained, 1.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    
    

    # Test different yearly interest rate
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_different_interest_rate(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 1, 1, 1, 1, 1, 6)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 2)
        self.assertEqual(returnedProjectionRow.totalContributions, 2)
        self.assertEqual(returnedProjectionRow.startingBalance, 1)
        self.assertEqual(returnedProjectionRow.currentBalance, 2.5)
        self.assertEqual(returnedProjectionRow.interestGained, 0.5)

        mock_update.assert_called_once()
        mock_add.assert_called_once()    
    

    # Test increasing the number of months 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_increasing_num_months(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 2, 1, 1, 1, 1, 0, 12)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[-1]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 2)
        self.assertEqual(returnedProjectionRow.numContributors, 1)
        self.assertEqual(returnedProjectionRow.individualContribution, 3)
        self.assertEqual(returnedProjectionRow.totalContributions, 3)
        self.assertEqual(returnedProjectionRow.startingBalance, 0)
        self.assertEqual(returnedProjectionRow.currentBalance, 4.0)
        self.assertEqual(returnedProjectionRow.interestGained, 1.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()


    # Test 1 month with other inputs changed from the base case 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_1_month_varied_input(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 1, 2, 1, 2, 2, 2, 6)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[0]
        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 1)
        self.assertEqual(returnedProjectionRow.numContributors, 2)
        self.assertEqual(returnedProjectionRow.individualContribution, 1)
        self.assertEqual(returnedProjectionRow.totalContributions, 4)
        self.assertEqual(returnedProjectionRow.startingBalance, 2)
        self.assertEqual(returnedProjectionRow.currentBalance, 5.0)
        self.assertEqual(returnedProjectionRow.interestGained, 1.0)

        mock_update.assert_called_once()
        mock_add.assert_called_once()

    
    # Test 3 months with the same input as the previous test case 
    @patch('helpers.addProjectionRows')
    @patch('helpers.updateProjectionFlags')
    def test_3_month_varied_input(self, mock_update, mock_add):

        mock_update.return_value = True
        mock_add.return_value = True
    
        returnVal = runProjection(1, 1, 3, 2, 1, 2, 2, 2, 6)
        
        self.assertTrue(type(returnVal) == list)

        returnedProjectionRow = returnVal[-1]

        self.assertEqual(returnedProjectionRow.projectionId, 1) 
        self.assertEqual(returnedProjectionRow.numMonths, 3)
        self.assertEqual(returnedProjectionRow.numContributors, 2)
        self.assertEqual(returnedProjectionRow.individualContribution, 3)
        self.assertEqual(returnedProjectionRow.totalContributions, 12)
        self.assertEqual(returnedProjectionRow.startingBalance, 2)
        self.assertEqual(returnedProjectionRow.currentBalance, 20.25)
        self.assertEqual(returnedProjectionRow.interestGained, 8.25)

        mock_update.assert_called_once()
        mock_add.assert_called_once()


if __name__ == '__main__':
    unittest.main()

