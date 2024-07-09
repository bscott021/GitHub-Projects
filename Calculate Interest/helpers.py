
import requests 
import ProjectionRow

def addProjectionRows(projectionRowList):
    """
    Add a list of ProjectionRow objects for interest calculations to a Coda document 
    
    Parameters:
        projectionRowList [ProjectionRow]: List of ProjectionRow objects to add
    
    Returns: None
    """

    authToken = "replace"

    basePath = "https://coda.io/apis/v1"
    docId = "replace"
    tableId = "replace"
    columnId1 = "replace"
    columnId2 = "replace"
    columnId3 = "replace"
    columnId4 = "replace"
    columnId5 = "replace"
    columnId6 = "replace"
    columnId7 = "replace"
    columnId8 = "replace"

    headers = {'Authorization': f'Bearer {authToken}'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'

    rows = []
    
    for r in projectionRowList:
        rows.append({'cells': [
            {'column': columnId1, 'value': r.projectionId},
            {'column': columnId2, 'value': r.numMonths},
            {'column': columnId3, 'value': r.numContributors},
            {'column': columnId4, 'value': r.individualContribution},
            {'column': columnId5, 'value': r.totalContributions},
            {'column': columnId6, 'value': r.startingBalance},
            {'column': columnId7, 'value': r.currentBalance},
            {'column': columnId8, 'value': r.interestGained}
        ]})
    
    payload = {
        'rows': rows
    }
    
    req = requests.post(uri, headers=headers, json=payload)
    req.raise_for_status() #TODO: Throw if there was an error.
    res = req.json()



def runProjection(projectionId, numMonths, numContributors, individualContribution, increaseAmount, numMonthsToIncrease, startingBalance, yearlyInterestRate):

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

        projectionSnapshot = ProjectionRow.ProjectionRow(projectionId, monthCount, numContributors, individualContribution, totalContributions, startingBalance, balance, totalInterestGained)
        projectionRows.append(projectionSnapshot)

    addProjectionRows(projectionRows)


