
import helpers as helpers


projectionQueue = helpers.getProjectionQueue()

if type(projectionQueue) != bool:
    
    for projection in projectionQueue: 

        if projection.generatedVal: 
            helpers.deleteProjectionRows(projection.projectionTitle)

        if projection.runVal:
            helpers.runProjection(projection.projectionHeaderRowId, projection.projectionTitle, projection.totalMonths, projection.contributors, projection.individualAmount, projection.increaseAmount, projection.monthsToIncrease, projection.startingBalance, projection.yearlyInterestRate)

else:
    print('Could not process projection: helpers.getProjectionQueue was not successful.')
