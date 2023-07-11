# import numeric
# from numeric import *
from problem import Numeric

# 그냥 좋은 것 찾는 것
LIMIT_STUCK = 100
# problem/Convex.txt


def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()  # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()


def firstChoice(p):
    current = p.randominit()  # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
    return current, valueC


def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())


main()
