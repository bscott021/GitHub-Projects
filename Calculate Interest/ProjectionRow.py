

class ProjectionRow:
    
    def __init__(self, projectionId, numMonths, numContributors, individualContribution, totalContributions, startingBalance, currentBalance, interestGained):
        """
        ProjectionRow object initialization of variables 
        
        Parameters: self 
            projectionId : Id value for the projection this row belongs to 
            numMonths Number : Number of months completed 
            numContributors Number : Amount of people who are contributing funds 
            individualContribution Number : The amount that each contributer is putting in monthly 
            totalContributions Number : Total number of contributions the group has made 
            startingBalance Number : Begining balance of the account 
            currentBalance Number : Current balance of the account 
            interestGained Number : Amount of interest gained from sitting in the account 
        """
        
        self.projectionId = projectionId
        self.numMonths = numMonths
        self.numContributors = numContributors
        self.individualContribution = individualContribution
        self.totalContributions = totalContributions
        self.startingBalance = startingBalance
        self.currentBalance = currentBalance
        self.interestGained = interestGained

