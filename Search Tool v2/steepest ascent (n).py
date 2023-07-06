# import numeric
# from numeric import *
from problem import Numeric

# problem/Convex.txt


def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()  # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()


def steepestAscent(p):
    current = p.randominit()  # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(p, neighbors)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def bestOf(p, neighbors):  ###
    best = neighbors[0]
    bestValue = p.evaluate(best)

    for i in range(1, len(neighbors)):
        newValue = p.evaluate(neighbors[i])
        if bestValue > newValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue


def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())


main()
