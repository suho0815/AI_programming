import random
import math


# interface
class Problem:
    def __init__(self):
        self._solution = []  # _변수 는 클래스 변수(private)임.
        self._value = 0
        self._numEval = 0

    def setVariables(self):  # createProblem
        pass

    def randominit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEvall))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)  ###
        self._expression = ""
        self._domain = []
        self._delta = 0.01

    def getDelta(self):
        return self._delta

    def setVariables(self):  # createProblem
        ## Read in an expression and its domain from a file.
        ## Then, return a problem 'p'.
        ## 'p' is a tuple of 'expression' and 'domain'.
        ## 'expression' is a string.
        ## 'domain' is a list of 'varNames', 'low', and 'up'.
        ## 'varNames' is a list of variable names.
        ## 'low' is a list of lower bounds of the varaibles.
        ## 'up' is a list of upper bounds of the varaibles.

        fileName = input("Enter the filename of a function :")
        infile = open(fileName, "r")
        self._expression = infile.readline()
        varName = []
        low = []
        up = []
        line = infile.readline()
        while line != "":
            temp = line.split(",")
            varName.append(temp[0])
            low.append(float(temp[1]))
            up.append(float(temp[2]))
            line = infile.readline()

        infile.close()
        self._domain = [varName, low, up]

    def randominit(self):
        domain = self._domain
        low = domain[1]
        up = domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r)

        return init  # Return a random initial point
        # as a list of values

    def evaluate(self, current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        self._numEval += 1
        expr = self._expression  # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + "=" + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain  # [VarNames, low, up]
        l = domain[1][i]  # Lower bound of i-th
        u = domain[2][i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):  ###
        i = random.randint(0, len(current) - 1)

        if random.uniform(0, 1) > 0.5:
            d = self._delta
        else:
            d = -self._delta

        return self.mutate(current, i, d)  # Return a random successor

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)

        return neighbors  # Return a set of successors

    def describe(self):
        print()
        print("Objective function:")
        print(self._domain[0])  # Expression
        print("Search space:")
        varNames = self._domain[1][0]  # p[1] is domain: [VarNames, low, up]
        low = self._domain[1][1]
        up = self._domain[1][2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value))
        Problem.report(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tupl


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []
        self._distanceTable = []

    def setVariables(self):  # createProblem
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, "r")
        # First line is number of cities
        self._numCities = int(infile.readline())
        self._locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != "":
            self._locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self._distanceTable = self.calcDistanceTable(self._numCities, self._locations)

    def calcDistanceTable(self):
        table = []
        locations = self._locations
        for i in range(self._numCities):
            row = []
            for j in range(self._numCities):
                dx = locations[i][0] - locations[j][0]
                dy = locations[i][1] - locations[j][1]
                d = round(math.sqrt(dx**2 + dy**2), 1)
                row.append(d)
            table.append(row)
        return table  # A symmetric matrix of pairwise distances

    def randominit(self):
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        self._numEval += 1
        cost = 0
        n = self._numCities
        table = self._distanceTable
        for i in range(n - 1):
            locFrom = current[i]
            locTo = current[i + 1]
            cost += table[locFrom][locTo]
        cost += table[current[n - 1]][current[0]]

        return cost

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def randomMutant(self, current):
        while True:
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end="")
            if i % 5 == 4:
                print()

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        Problem.report(self)

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end="")
            if i % 10 == 9:
                print()
