

# Todo: Add tests and some better print statements. Improve the formatting and possibly allow posting to coda.

numContributers = 5
monthlyContribution = 150
numMonths = 84
monthlyRate = 0.05/12

increaseAmount = 0
numMonthsIncrease = 12

balance = 10000

print(f'Contributers: {numContributers}')
print(f'Monthly contribution per persion: {monthlyContribution}')
print(f'Number of months: {numMonths}')
print(f'Monthly Interest Rate: {monthlyRate}')
print(f'Starting balance: {balance}')

monthCount = 0

for i in range(0, numMonths):
    totalMonthlyContribution = numContributers * monthlyContribution
    interestGained = balance * monthlyRate
    balance += totalMonthlyContribution + interestGained

    monthCount += 1

    if monthCount == numMonthsIncrease:
        monthlyContribution += increaseAmount
        print(f'New Contribution Amount: {monthlyContribution}')
        monthCount = 0

print(f'Ending balance: {balance}')
