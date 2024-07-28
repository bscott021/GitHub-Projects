

class ProjectionHeader:
    
    def __init__(self, projectionHeaderRowId, runVal, generatedVal, projectionTitle, totalMonths, contributors, individualAmount, increaseAmount, monthsToIncrease, startingBalance, yearlyInterestRate):
        """
        ProjectionRow object initialization of variables
        
        Parameters: self
            runVal : On/off value to determine if projection should be run/generated
            generatedVal : Flag to tell if projection has already been generated 
            projectionTitle : Title of projections 
            totalMonths : Number of months for projection
            econtributors : Number of contributors 
            individualAmount : Individual contribution amount 
            increaseAmount : Amount to increase contributions by 
            monthsToIncrease : How often to increase contributions (in months)
            startingBalance : Starting balance of the account 
            yearlyInterest : Yearly interest rate 
        """
        
        self.projectionHeaderRowId = projectionHeaderRowId
        self.runVal = runVal
        self.generatedVal = generatedVal
        self.projectionTitle = projectionTitle
        self.totalMonths = totalMonths
        self.contributors = contributors
        self.individualAmount = individualAmount
        self.increaseAmount = increaseAmount
        self.monthsToIncrease = monthsToIncrease
        self.startingBalance = startingBalance
        self.yearlyInterestRate = yearlyInterestRate
    

