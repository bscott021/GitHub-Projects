
class ProjectionRow:
    
    def __init__(self, numMonths, numContributors, individualContribution, totalContributions, startingBalance, currentBalance, interestGained):
        """
        ProjectionRow object initialization of variables
        
        Parameters: self
            numMonths Number: 
            numContributors Number: 
            individualContribution Number: 
            totalContributions Number: 
            startingBalance Number: 
            currentBalance Number: 
            interestGained Number: 
        """
        
        self.numMonths = numMonths
        self.numContributors = numContributors
        self.individualContribution = individualContribution
        self.totalContributions = totalContributions
        self.startingBalance = startingBalance
        self.currentBalance = currentBalance
        self.interestGained = interestGained

