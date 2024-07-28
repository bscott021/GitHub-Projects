
import os
import json
import requests 

import Classes.ProjectionHeader
import Classes.ProjectionRow


def loadConfig(configFile='Calculate Interest/config.json'):
    """
    Load the config file values 
    
    Parameters:
        configFile : Full file path to config file
    
    Returns: Config file json
    """
    
    try: 
        with open(configFile, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing file '{configFile}': {e}")
    except (ValueError, TypeError) as e:
        print(f"Invalid data in file '{configFile}': {e}")
    except Exception as e:
        print(f"Unexpected error reading file '{configFile}': {e}")


def updateProjectionFlags(rowId, runVal, generatedVal):

    # Check for valid run status and generated status'
    if type(runVal) != bool or type(generatedVal) != bool:
        # TODO: Add better message here 
        return

    # Get API Token
    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")

    # Get Cofig values and put if successful 
    try:
        config = loadConfig()

        basePath = config['basePath']
        docId = config['docId']
        tableId = config['projectionHeaderTableId']

        runColId = config['runColId']
        generatedColId = config['generatedColId']


        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows/{rowId}'
        
        payload = {
            'row': {
                'cells': [
                    {'column': runColId, 'value': runVal},
                    {'column': generatedColId, 'value': generatedVal}
                ],
            },
        }
        
        req = requests.put(uri, headers=headers, json=payload)
        req.raise_for_status() #TODO: Throw if there was an error.
        res = req.json()

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during addProjectionRows: {e}")
        exit(1)



def addProjectionRows(projectionRowList):
    """
    Add a list of ProjectionRow objects for interest calculations to a Coda document 
    
    Parameters:
        projectionRowList [ProjectionRow]: List of ProjectionRow objects to add
    
    Returns: None
    """

    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")

    try:
        config = loadConfig()

        basePath = config['basePath']
        docId = config['docId']
        tableId = config['projectionDataTableId']

        projectionTextColId = config['projectionTextColId']
        numMonthsColId = config['numMonthsColId']
        numContributorsColId = config['numContributorsColId']
        individualContributionColId = config['individualContributionColId']
        totalContributionsColId = config['totalContributionsColId']
        startingBalanceColId2 = config['startingBalanceColId2']
        currentBalanceColId = config['currentBalanceColId']
        interestGainedColId = config['interestGainedColId']

        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'

        rows = []
        
        for r in projectionRowList:
            rows.append({'cells': [
                {'column': projectionTextColId, 'value': r.projectionId},
                {'column': numMonthsColId, 'value': r.numMonths},
                {'column': numContributorsColId, 'value': r.numContributors},
                {'column': individualContributionColId, 'value': r.individualContribution},
                {'column': totalContributionsColId, 'value': r.totalContributions},
                {'column': startingBalanceColId2, 'value': r.startingBalance},
                {'column': currentBalanceColId, 'value': r.currentBalance},
                {'column': interestGainedColId, 'value': r.interestGained}
            ]})
        
        payload = {
            'rows': rows
        }
        
        req = requests.post(uri, headers=headers, json=payload)
        req.raise_for_status() #TODO: Throw if there was an error.
        res = req.json()

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during addProjectionRows: {e}")
        exit(1)



def deleteProjectionRows(projectionText):

    # Get API Token
    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")

    try:
        config = loadConfig()

        basePath = config['basePath']
        docId = config['docId']
        tableId = config['projectionDataTableId']

        projectionTextColId = config['projectionTextColId']

        headers = {'Authorization': f'Bearer {authToken}'}

        # Get the projection data rows to get the ids the need to be deleted 
        uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'
        res = requests.get(uri, headers=headers).json()
        
        returnedItems = res["items"]

        rowIdsToDelete = []
        
        for projectionData in returnedItems:
            
            projectionDataRowId = projectionData["id"]
            projectionDataRow = projectionData["values"]
            
            runCprojectionTextColVal = projectionDataRow[projectionTextColId]

            # Add row ids if the prjoection = the header prjection passed in 
            if projectionText == runCprojectionTextColVal:
                rowIdsToDelete.append(projectionDataRowId)

        # Create payload and delete the rows from the table 
        payload = {
            'rowIds': rowIdsToDelete,
        }

        req = requests.delete(uri, headers=headers, json=payload)
        req.raise_for_status() # Throw if there was an error.
        res = req.json()

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during addProjectionRows: {e}")
        exit(1)



def getProjectionQueue():
    """
    Get the projetion rows that are ready to run
    
    Parameters: None
    
    Returns:
        [ProjectionHeader]: List of ProjectionHeader objects in run status
    """

    authToken = os.getenv('authToken')

    if not authToken:
        raise ValueError("Missing environment variable: authToken")

    runProjections = []

    try:
        config = loadConfig()

        basePath = config['basePath']
        docId = config['docId']
        tableId = config['projectionHeaderTableId']

        runColId = config['runColId']
        generatedColId = config['generatedColId']
        projetionColId = config['projetionColId']
        totalMonthsColId = config['totalMonthsColId']
        contributorsColId = config['contributorsColId']
        individualAmountColId = config['individualAmountColId']
        increaseAmountColId = config['increaseAmountColId']
        monthsToIncreaseColId = config['monthsToIncreaseColId']
        startingBalanceColId = config['startingBalanceColId']
        yearlyInterestRateColId = config['yearlyInterestRateColId']
        
        headers = {'Authorization': f'Bearer {authToken}'}
        uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'
        res = requests.get(uri, headers=headers).json()
        
        returnedItems = res["items"]
        
        for projectionHeader in returnedItems:
            
            projectionHeaderRowId = projectionHeader["id"]
            runProjectionRow = projectionHeader["values"]
            
            runColVal = runProjectionRow[runColId]
            generatedColVal = runProjectionRow[generatedColId]
            projetionColVal = runProjectionRow[projetionColId]
            totalMonthsColVal = runProjectionRow[totalMonthsColId]                
            contributorsColVal = runProjectionRow[contributorsColId]
            individualAmountColVal = runProjectionRow[individualAmountColId]
            increaseAmountColVal = runProjectionRow[increaseAmountColId]
            monthsToIncreaseColVal = runProjectionRow[monthsToIncreaseColId] 
            startingBalanceColVal = runProjectionRow[startingBalanceColId]
            yearlyInterestRateColVal = runProjectionRow[yearlyInterestRateColId]

            if runColVal:
                runProjections.append(Classes.ProjectionHeader.ProjectionHeader(projectionHeaderRowId, runColVal, generatedColVal, projetionColVal, totalMonthsColVal, contributorsColVal, individualAmountColVal, increaseAmountColVal, monthsToIncreaseColVal, startingBalanceColVal, yearlyInterestRateColVal))

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading configuration during getProjectionQueue: {e}")
        exit(1)

    return runProjections



def runProjection(projectionHeaderRowId, projectionId, numMonths, numContributors, individualContribution, increaseAmount, numMonthsToIncrease, startingBalance, yearlyInterestRate):

    """
    Calculate the projection data for a single projection and add the rows to Coda
    
    Parameters:
        projectionId Number: Unique identifier for this projection 
        numMonths Number: Number of months to run the projection for 
        numContributors Number: Number of people contributing to the account 
        individualContribution Number: Amount each person is contributing 
        increaseAmount Number: Amount to increase the individual contribution amount 
        numMonthsToIncrease Number: Number of months to wait before increasing the contribution amount 
        startingBalance Number: Starting balnce 
        yearlyInterestRate Number: Annual interest rate on the account 
    
    Returns: None
    """

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

        projectionSnapshot = Classes.ProjectionRow.ProjectionRow(projectionId, monthCount, numContributors, individualContribution, totalContributions, startingBalance, balance, totalInterestGained)
        projectionRows.append(projectionSnapshot)

    # Add the projection rows to the table 
    addProjectionRows(projectionRows)

    # Mark the projection header as generated and deselect the run flag 
    updateProjectionFlags(projectionHeaderRowId, False, True)

