# from tsp import *
from problem import Tsp

# 외판원문제
# TSP 알고리즘: 도시의 개수와 각 도시 쌍 간의 거리들이 주어질 때, 모든 도시를 한 번씩 방문하고
#  여행을 시작한 원래 도시로 돌아올 수 있는 최단거리 경로(Shortest distance path)를 구하라

# problem/tsp30.txt
# problem/tsp50.txt
# problem/tsp100.txt


def main():
    # Create an instance of TSP
    p = Tsp()
    p.setVariables()  # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting()
    # Report results
    p.report()


def steepestAscent(p):
    current = p.randominit()  # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = p.bestOf(neighbors)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")


main()
