
import helpers


projectionQueue = helpers.getProjectionQueue()


for projection in projectionQueue: 

    if projection.generatedVal: 
        #TODO: Delete the old projection data 
        print('Start here')

    if projection.runVal:
        helpers.runProjection(projection.projectionHeaderRowId, projection.projectionTitle, projection.totalMonths, projection.contributors, projection.individualAmount, projection.increaseAmount, projection.monthsToIncrease, projection.startingBalance, projection.yearlyInterestRate)
    
