from tsp import *

#외판원문제
#TSP 알고리즘: 도시의 개수와 각 도시 쌍 간의 거리들이 주어질 때, 모든 도시를 한 번씩 방문하고
#  여행을 시작한 원래 도시로 돌아올 수 있는 최단거리 경로(Shortest distance path)를 구하라

#problem/tsp30.txt
#problem/tsp50.txt
#problem/tsp100.txt

def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)

def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
