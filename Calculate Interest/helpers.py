
import os
import json
import requests 

import ProjectionHeader
from ProjectionRow import ProjectionRow


def loadConfig(configFilePath='config.json'):
    """
    Load the config file values 
    
    Parameters:
        configFilePath : Full file path to config file
    
    Returns: Config file json
    """
    
    try: 
        with open(configFilePath, 'r') as file:
            return json.load(file)
        
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing file '{configFilePath}': {e}")

    except (ValueError, TypeError) as e:
        print(f"Invalid data in file '{configFilePath}': {e}")

    except Exception as e:
        print(f"Unexpected error reading file '{configFilePath}': {e}")


def updateProjectionFlags(rowId, runVal, generatedVal):
    """
    Update the projection flags in the Projection Header table 
    
    Parameters:
        rowId str : Row id used to update flags
        runVal bool : Value to determine if the projection should be run 
        generatedVal bool : Value to track if the projection has been generated 
    
    Returns: True for a successful call and False otherwise
    """

    invalidInput = []

    if type(rowId) != str:
        invalidInput.append(f'rowId expected str got: {rowId} ({type(rowId)})')

    if type(runVal) != bool:
        invalidInput.append(f'runVal expected bool got: {runVal} ({type(runVal)})')

    if type(generatedVal) != bool:
        invalidInput.append(f'generatedVal expected bool got: {generatedVal} ({type(generatedVal)})')


    if invalidInput != []:
        print(f'Invalid Input:')
        for i in invalidInput:
            print(i)
        print()
        return False

    
    authToken = os.getenv('authToken')

    if not authToken:
        print('Missing environment variable: authToken')
        return False

    
    config = loadConfig()

    if config:

        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{config['basePath']}/docs/{config['docId']}/tables/{config['projectionHeaderTableId']}/rows/{rowId}'
        
        payload = {
            'row': {
                'cells': [
                    {'column': config['runColId'], 'value': runVal},
                    {'column': config['generatedColId'], 'value': generatedVal}
                ],
            },
        }
        
        req = requests.put(uri, headers=headers, json=payload)
        req.raise_for_status()
        res = req.json()    

        try:
            res['requestId']
            return True
        except:
            print(f'HTTP Error Code: {res['statusCode']} - {res['statusMessage']}')

    return False


def addProjectionRows(projectionRowList):
    """
    Add a list of ProjectionRow objects for interest calculations to a Coda document.
    Any items in the list that are not ProjectionRow objects will not be added
    
    Parameters:
        projectionRowList [ProjectionRow]: List of ProjectionRow objects to add
    
    Returns: True if successful, False otherwise 
    """

    if type(projectionRowList) != list:
        return False

    authToken = os.getenv('authToken')

    if not authToken:
        print('Missing environment variable: authToken')
        return False

    config = loadConfig()

    if config:

        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{config['basePath']}/docs/{config['docId']}/tables/{config['projectionDataTableId']}/rows'

        rows = []
        
        for r in projectionRowList:
            if isinstance(r, ProjectionRow): 
                rows.append({'cells': [
                    {'column': config['projectionTextColId'], 'value': r.projectionId},
                    {'column': config['numMonthsColId'], 'value': r.numMonths},
                    {'column': config['numContributorsColId'], 'value': r.numContributors},
                    {'column': config['individualContributionColId'], 'value': r.individualContribution},
                    {'column': config['totalContributionsColId'], 'value': r.totalContributions},
                    {'column': config['startingBalanceColId2'], 'value': r.startingBalance},
                    {'column': config['currentBalanceColId'], 'value': r.currentBalance},
                    {'column': config['interestGainedColId'], 'value': r.interestGained}
                ]})
        
        if rows != []:
            payload = {
                'rows': rows
            }

            req = requests.post(uri, headers=headers, json=payload)
            req.raise_for_status()
            res = req.json()

            try:
                res['requestId']
                return True
            except:
                print(f'HTTP Error Code: {res['statusCode']} - {res['statusMessage']}')

    return False


def deleteProjectionRows(projectionText):
    """
    Delete projection rows for a certain ProjectionText value 
    
    Parameters str: projectionText
    
    Returns: 
        True: When the delete was successful or there was nothing to delete 
        False: When there was a problem with trying to delete
    """

    if type(projectionText) != str or len(projectionText) < 1:
        return False


    authToken = os.getenv('authToken')

    if not authToken:
        print('Missing environment variable: authToken')
        return False

    config = loadConfig()

    if config:

        headers = {'Authorization': f'Bearer {authToken}'}

        uri = f'{config['basePath']}/docs/{config['docId']}/tables/{config['projectionDataTableId']}/rows'
        res = requests.get(uri, headers=headers).json()

        try:
            returnedItems = res["items"]

            if returnedItems != []:

                rowIdsToDelete = []

                for projectionData in returnedItems:

                    projectionDataRow = projectionData["values"]
                    
                    runProjectionTextColVal = projectionDataRow[config['projectionTextColId']]

                    if projectionText == runProjectionTextColVal:
                        rowIdsToDelete.append(projectionData["id"])

                payload = {
                    'rowIds': rowIdsToDelete,
                }

                req = requests.delete(uri, headers=headers, json=payload)
                req.raise_for_status()
                res = req.json()

                try:
                    res['requestId']
                    # Delete Succeeded
                    return True

                except:
                    # Error from Delete Request
                    print(f'HTTP Error Code: {res['statusCode']} - {res['statusMessage']}')

            else:
                # Nothing to delete
                return True

        except:
            # Error from Get Request 
            print(f'HTTP Error Code: {res['statusCode']} - {res['statusMessage']}')

    return False


def getProjectionQueue():
    """
    Get the projetion rows that are ready to run
    
    Parameters: None
    
    Returns:
        When Successful: 
            [ProjectionHeader]: List of ProjectionHeader objects in run status
        Else:
            False: The projection queue did not return 
    """

    authToken = os.getenv('authToken')

    if not authToken:
        print('Missing environment variable: authToken')
        return False

    runProjections = []
    config = loadConfig()

    if config: 
        
        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{config['basePath']}/docs/{config['docId']}/tables/{config['projectionHeaderTableId']}/rows'
        res = requests.get(uri, headers=headers).json()

        try:
            returnedItems = res["items"]
        
            for projectionHeader in returnedItems:
                
                projectionHeaderRowId = projectionHeader["id"]
                runProjectionRow = projectionHeader["values"]
                
                runColVal = runProjectionRow[config['runColId']]

                if runColVal:
                    runProjections.append(ProjectionHeader.ProjectionHeader(projectionHeaderRowId, runColVal, runProjectionRow[config['generatedColId']], runProjectionRow[config['projetionColId']], runProjectionRow[config['totalMonthsColId']], runProjectionRow[config['contributorsColId']], runProjectionRow[config['individualAmountColId']], runProjectionRow[config['increaseAmountColId']], runProjectionRow[config['monthsToIncreaseColId']], runProjectionRow[config['startingBalanceColId']], runProjectionRow[config['yearlyInterestRateColId']]))
            
            if runProjections != []:
                return runProjections

        except:
            print(f'HTTP Error Code: {res['statusCode']} - {res['statusMessage']}')
    
    return False 


def runProjection(projectionHeaderRowId, projectionId, numMonths, numContributors, individualContribution, increaseAmount, numMonthsToIncrease, startingBalance, yearlyInterestRate):
    """
    Calculate the projection data for a single projection and add the rows to Coda
    
    Parameters:
        projectionHeaderRowId String : Row id of the projection header passed in
        projectionId : Unique identifier for this projection 
        numMonths Number: Number of months to run the projection for 
        numContributors Number: Number of people contributing to the account 
        individualContribution Number: Amount each person is contributing 
        increaseAmount Number: Amount to increase the individual contribution amount 
        numMonthsToIncrease Number: Number of months to wait before increasing the contribution amount 
        startingBalance Number: Starting balnce 
        yearlyInterestRate Number: Annual interest rate on the account 
    
    Returns: 
        [ProjectionRow] List of projection rows for this projection
            OR
        [] If it was not added to Coda
    """

    if numMonths < 1:
        print(f'The number of months must be greater than 0')
        return []

    monthlyRate = yearlyInterestRate/12
    balance = startingBalance
    totalContributions = startingBalance
    totalInterestGained = 0

    monthCountIncrease = 0
    monthCount = 0
    projectionRows = []

    for i in range(0, numMonths):
        
        totalMonthlyContribution = numContributors * individualContribution
        totalContributions += totalMonthlyContribution

        interestGained = balance * monthlyRate
        totalInterestGained += interestGained

        balance += totalMonthlyContribution + interestGained

        monthCount += 1
        monthCountIncrease += 1

        if monthCountIncrease == numMonthsToIncrease:
            individualContribution += increaseAmount
            monthCountIncrease = 0

        projectionSnapshot = ProjectionRow(projectionId, monthCount, numContributors, individualContribution, totalContributions, startingBalance, balance, totalInterestGained)
        projectionRows.append(projectionSnapshot)

    addResult = addProjectionRows(projectionRows)

    updateFlagsResult = updateProjectionFlags(projectionHeaderRowId, False, True)

    if addResult and updateFlagsResult:
        return projectionRows
    
    return []

