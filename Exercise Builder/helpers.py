
def none(checkList):
    """
    Checks to see if all the items in the list are empty strings
    
    Parameters:
        checkList [String]: The List of strings you wish to check
    
    Returns:
        Bool:
            True when all items in the list are ""
            False when at least one item in the list is not ""
    """

    for item in checkList:

        if item != "":
            return False

    return True


def all(checkList):
    """
    Checks to see if all the items in the list are strings of at least one character
    
    Parameters:
        checkList [String]: The List of strings you wish to check
    
    Returns:
        Bool:
            True when all items in the list are not ""
            False when at least one item in the list is not ""
    """

    if len(checkList) == 0:
        return False
    
    for item in checkList:
        
        if item == "":
            return False

    return True

