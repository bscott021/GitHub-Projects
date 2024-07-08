
import ProjectionRow
import requests 

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

    headers = {'Authorization': f'Bearer {authToken}'}
    uri = f'{basePath}/docs/{docId}/tables/{tableId}/rows'

    rows = []
    
    for r in projectionRowList:
        rows.append({'cells': [
            {'column': columnId1, 'value': r.numMonths},
            {'column': columnId2, 'value': r.numContributors},
            {'column': columnId3, 'value': r.individualContribution},
            {'column': columnId4, 'value': r.totalContributions},
            {'column': columnId5, 'value': r.startingBalance},
            {'column': columnId6, 'value': r.currentBalance},
            {'column': columnId7, 'value': r.interestGained}
        ]})
    
    payload = {
        'rows': rows
    }
    
    req = requests.post(uri, headers=headers, json=payload)
    req.raise_for_status() # Throw if there was an error.
    res = req.json()


numMonths = 84
numContributors = 4
individualContribution = 150
balance = 5667

monthlyRate = 0.05/12
increaseAmount = 50
numMonthsToIncrease = 12

startingBalance = balance
totalContributions = balance
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
        # print(f'New Contribution Amount: {individualContribution}')
        monthCountIncrease = 0

    projectionSnapshot = ProjectionRow.ProjectionRow(monthCount, numContributors, individualContribution, totalContributions, startingBalance, balance, totalInterestGained)
    projectionRows.append(projectionSnapshot)

# print(f'Ending balance: {balance}')

addProjectionRows(projectionRows)

