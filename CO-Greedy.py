import copy
import time
import numpy

class Street:
    def __init__(self, id, start, end, name, duration):
        self.id = id
        self.start = start
        self.end = end
        self.name = name
        self.duration = duration

class Inter:
    def __init__(self, name):
        self.name = name
        self.incoming = []
        self.timetable = []

class Car:
    def __init__(self, id, start, path):
        self.id = id
        self.start = start
        self.path = path
        self.curState = path[1]
        self.driving = 0
        self.waiting = 0

def problemSimulation():
    duration, noInters, noStreets, noCars, bonus = list(map(int, input().split()))
    streets = {}
    cars = []
    inters = {}
    for i in range(noInters):
        inters[i] = Inter(i)
    for i in range(noStreets):
        data = input().split()
        streets[data[2]] = Street(i, int(data[0]), int(data[1]), data[2], int(data[3]))
        inters[int(data[1])].incoming.append(data[2])
    for i in range(noCars):
        data = input().split()
        path = []
        for j in range(len(data[1:])):
            path.append(data[1:][j])
            path.append(int(streets[data[1:][j]].end))
        cars.append(Car(i, data[1], path))
    return streets, duration, noInters, noStreets, noCars, bonus, cars, inters

def greedySolution(inters):
    solution = {}
    for intersection in inters:
        solution[intersection] = {}
        kopia = copy.deepcopy(inters[intersection].incoming)
        numpy.random.shuffle(kopia)
        for inc in kopia:
            solution[intersection][inc] = 1
    return solution

def printSolution(solution):
    print(str(len(solution)))
    for intersection in solution:
        print(str(intersection))
        print(str(len(solution[intersection])))
        for j in solution[intersection]:
            print(str(j) + " " + str(solution[intersection][j]))

def main():
    start = time.time()
    streets, duration, noInters, noStreets, noCars, bonus, cars, inters = problemSimulation()
    printSolution(greedySolution(inters))
    print('\n')
    end = time.time()
    print('Time to obtain the result: ', round(end - start, 3), 'sec')

main()
