
import helpers
import ProjectionRow

projectionId = 5
numMonths = 24
numContributors = 1
individualContribution = 1500
balance = 10000
increaseAmount = 0
numMonthsToIncrease = 0

monthlyRate = 0.05/12
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

    projectionSnapshot = ProjectionRow.ProjectionRow(projectionId, monthCount, numContributors, individualContribution, totalContributions, startingBalance, balance, totalInterestGained)
    projectionRows.append(projectionSnapshot)

# print(f'Ending balance: {balance}')

helpers.addProjectionRows(projectionRows)

