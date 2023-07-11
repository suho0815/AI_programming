# from tsp import *
from problem import Tsp

LIMIT_STUCK = 100
# problem/tsp30.txt
# problem/tsp50.txt
# problem/tsp100.txt


def main():
    # Create an instance of TSP
    p = Tsp()
    p.setVariables()  # 'p': (numCities, locations, distanceTable)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting()
    # Report results
    p.report()


def firstChoice(p):
    current = p.randominit()  # 'current' is a list of city ids
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


def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")


main()
