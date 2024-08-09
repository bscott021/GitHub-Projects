

class ProjectionHeader:
    
    def __init__(self, projectionHeaderRowId, runVal, generatedVal, projectionTitle, totalMonths, contributors, individualAmount, increaseAmount, monthsToIncrease, startingBalance, yearlyInterestRate):
        """
        Projection Header Object
        
        Parameters: self
            runVal Bool : Flag to determine if projection should be run/generated
            generatedVal Bool : Flag to tell if projection has already been generated 
            projectionTitle String : Title of projections 
            totalMonths Number : Number of months for projection
            contributors Number : Number of contributors 
            individualAmount Number : Individual contribution amount 
            increaseAmount Number : Amount to increase contributions by 
            monthsToIncrease Number : How often to increase contributions (in months)
            startingBalance Number : Starting balance of the account 
            yearlyInterestRate Number : Yearly interest rate 
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
    

