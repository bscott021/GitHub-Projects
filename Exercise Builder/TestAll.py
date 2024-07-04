
import unittest
import helpers



class TestAll(unittest.TestCase):
    """
    Test the all() function defined in helpers
    """

    def test_empty_list(self):
        """ Test Empty List : Expects False """
        result = helpers.all([])
        assert not result
    
    def test_one_element_empty(self):
        """ 1 element list that contains an empty string : Expects False """
        result = helpers.all([""])
        assert not result
    
    def test_one_element_not_empty(self):
        """ 1 element list that contains a string : Expects True """
        result = helpers.all(["A"])
        assert result
    
    def test_two_elements_both_empty(self):
        """ 2 element list with both as empty strings : Expects False """
        result = helpers.all(["", ""])
        assert not result
    
    def test_two_elements_not_empty(self):
        """ 2 element list with both as string values : Expects True """
        result = helpers.all(["A", "B"])
        assert result
    
    def test_two_elements_first_empty(self):
        """ 2 element list with the first element as an empty string but not the second : Expects False """
        result = helpers.all(["", "B"])
        assert not result
    
    def test_two_elements_second_empty(self):
        """ 2 element list with the second element as an empty string but not the first : Expects False """
        result = helpers.all(["A", ""])
        assert not result
    

if __name__ == '__main__':
    unittest.main()
