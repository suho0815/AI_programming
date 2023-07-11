from problem import Numeric


# problem/Convex.txt
# problem/Ackley.txt
# problem/Griewank.txt
def main():
    # Create an instance of numerical optimization problem
    p = Numeric()
    p.setVariables()
    # Call the search algorithm
    solution, minimum = gradientDescent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()


def gradientDescent(p):
    current = p.randominit()  # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        successor = p.takeStep(current, valueC)
        valueS = p.evaluate(successor)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def bestOf(neighbors, p):
    best = neighbors[0]  # 'best' is a value list
    bestValue = p.evaluate(최고)
    for i in range(1, len(neighbors)):
        newValue = p.evaluate(neighbors[i])
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue
    return best, bestValue


def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())


main()
