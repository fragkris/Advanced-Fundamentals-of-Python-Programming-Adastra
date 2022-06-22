import math

nums = [-3, -5, 1, 4]

def logistic(x):
    for i in x:
        print(round(1 / (1 + math.exp(-i)), 4))

logistic(nums)
print()

# ^ Using normal function


logisticFunc = lambda arr: list(map(lambda x: print(round(1/(1+math.exp(-x)), 4)), arr))
logisticFunc(nums)

# ^ Using lambda function

