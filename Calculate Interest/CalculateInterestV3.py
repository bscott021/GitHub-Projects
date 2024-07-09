
import helpers


"""
    TODO: Get input values and run multiple projections based on the parameters. Dynamically assign projection id 
"""

projectionId = 5
numMonths = 12
numContributors = 4
individualContribution = 150
increaseAmount = 100
numMonthsToIncrease = 24
startingBalance = 6667
yearlyInterestRate = 0.05


helpers.runProjection(projectionId, numMonths, numContributors, individualContribution, increaseAmount, numMonthsToIncrease, startingBalance, yearlyInterestRate)

