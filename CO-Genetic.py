import copy
import random
import time
import numpy

class Street:
    def __init__(self, start, end, name, duration):
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
        streets[data[2]] = Street(int(data[0]), int(data[1]), data[2], int(data[3]))
        inters[int(data[1])].incoming.append(data[2])
    for i in range(noCars):
        data = input().split()
        path = []
        for j in range(len(data[1:])):
            path.append(data[1:][j])
            path.append(int(streets[data[1:][j]].end))
        cars.append(Car(i, data[1], path))
    return streets, duration, noInters, noStreets, noCars, bonus, cars, inters

def printSolution(solution):
    print(str(len(solution)))
    for intersection in solution:
        print(str(intersection))
        print(str(len(solution[intersection])))
        for j in solution[intersection]:
            print(str(j) + " " + str(solution[intersection][j]))

def heuristic(duration, initCars, initStreets, solution, points, initInters):
    cars = copy.deepcopy(initCars)
    streets = copy.deepcopy(initStreets)
    inters = copy.deepcopy(initInters)
    for i in solution:
        for j in solution[i]:
            for k in range(solution[i][j]):
                inters[i].timetable.append(j)
    score = 0
    queue = {x: {y: list() for y in inters[x].incoming} for x in inters}
    for sec in range(1, duration + 1):
        for car in cars:
            if isinstance(car.curState, int):
                if car not in queue[car.curState][car.path[car.path.index(car.curState) - 1]]:
                    queue[car.curState][car.path[car.path.index(car.curState) - 1]].append(car)
                if car.path[car.path.index(car.curState) - 1] == inters[car.curState].timetable[sec % len(inters[car.curState].timetable) - 1] and queue[car.curState][car.path[car.path.index(car.curState) - 1]][0] == car:
                    queue[car.curState][car.path[car.path.index(car.curState) - 1]].remove(car)
                    car.curState = car.path[car.path.index(car.curState) + 1]
                    car.driving = streets[car.curState].duration
                    continue
            if not isinstance(car.curState, int):
                if car.driving != 0:
                    car.driving -= 1
                if car.driving == 0:
                    car.curState = car.path[car.path.index(car.curState) + 1]
            if car.curState == car.path[-1]:
                score += points + (duration - sec + 1)
                cars.remove(cars[cars.index(car)])
    return score

def genetic(duration, cars, streets, points, inters, start):
    def createIndividual(inters):
        solution = {}
        for intersection in inters:
            solution[intersection] = {}
            kopia = copy.deepcopy(inters[intersection].incoming)
            numpy.random.shuffle(kopia)
            for inc in kopia:
                solution[intersection][inc] = 1
        return solution

    def fitness(duration, cars, streets, individual, points, inters):
        return heuristic(duration, cars, streets, individual, points, inters)

    def mutation(individual):
        for i in range(len(individual)//20 + 1):
            selectedInter = random.randint(0, len(individual) - 1)
            for street in individual[selectedInter]:
                individual[selectedInter][street] = random.randint(1, duration // len(individual[selectedInter]))
        return individual

    def crossOver(parent1, parent2):
        cuttingPoint = random.randint(0, len(parent1) - 1)
        part1 = {y: parent1[y] for y in range(cuttingPoint)}
        part2 = {y: parent2[y] for y in range(cuttingPoint, len(parent2))}
        child = {}
        child.update(part1)
        child.update(part2)
        return child

    def tournament(population):
        matingPoolSize = 3
        matingPool = []
        for i in range(matingPoolSize):
            matingPool.append(population[random.randint(0, len(population) - 1)])
        matingPool = sorted(matingPool, key=lambda x: x[1], reverse=True)
        return matingPool[0][0]

    popSize = 20
    population = [list() for i in range(popSize)]
    for i in range(popSize):
        if time.time() - start > 250:
            return population[0]
        individual = createIndividual(inters)
        population[i].append(individual)
        population[i].append(fitness(duration, cars, streets, individual, points, inters))
    population = sorted(population, key=lambda x: x[1], reverse=True)

    noImprove = 0
    best = population[0][1]
    while noImprove < 5:
        children = [list() for x in range(popSize)]
        j = 0
        while j < popSize:
            if time.time() - start > 250:
                return population[0]
            child = mutation(tournament(population))
            children[j].append(child)
            children[j].append(fitness(duration, cars, streets, child, points, inters))
            child = crossOver(tournament(population), tournament(population))
            children[j+1].append(child)
            children[j+1].append(fitness(duration, cars, streets, child, points, inters))
            j += 2
        population += children
        population = sorted(population, key=lambda x: x[1], reverse=True)
        population = population[:popSize]
        if best == population[0][1]:
            noImprove += 1
        if population[0][1] > best:
            best = population[0][1]
            noImprove = 0
    return population[0]

def main():
    start = time.time()
    streets, duration, noInters, noStreets, noCars, bonus, cars, inters = problemSimulation()
    printSolution(genetic(duration, cars, streets, bonus, inters, start)[0])
    print('\n')
    end = time.time()
    print('Time to obtain the result: ', round(end - start, 3), 'sec')

main()
