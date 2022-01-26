# Combinatorial Optimization Lab Project
## Heuristic algorithms (namely, Greedy and Genetic) for solving Traffic Signaling Problem 
### Prepared by students of WIiT, AI, 3rd Semester, SI4: Uladzimir Ivashka, 150281, and Sofya Aksenyuk, 150284
#### Programs are written in Python 3.10

**To run the files it is adviced to simply enter the initial data from _stdin_ in a following way, e.g.:**

```
6 4 5 2 1000
2 0 rue-de-londres 1
0 1 rue-d-amsterdam 1
3 1 rue-d-athenes 1
2 3 rue-de-rome 2
1 2 rue-de-moscou 3
4 rue-de-londres rue-d-amsterdam
rue-de-moscou rue-de-rome
3 rue-d-athenes rue-de-moscou
rue-de-londres
```

**Where:**

```
The simulation lasts 6 seconds, there are 4
intersections, 5 streets, and 2 cars; and a car
scores 1000 points for reaching the destination
on time.
Street rue-de-londres starts at intersection 2,
ends at 0, and it takes L=1 seconds to go from
the beginning to the end.
Street rue-d-amsterdam starts at intersection 0,
ends at 1 and has L=1.
Street rue-d-athenes starts at intersection 3,
ends at 1 and has L=1.
Street rue-de-rome starts at intersection 2,
ends at 3 and has L=2.
Street rue-de-moscou starts at intersection 1,
ends at 2, and has L=3.
The first car starts at the end of
rue-de-londres and then follows the given path.
The second car starts at the end of
rue-d-athenes and then follows the given path.
```

**The solution to the problem gets shown as _stdout_**


## Theoretical part (methods that were used):

**As a simple approach to the problem Greedy Algorithm was used since:**

- it is straightforward to implement
- it finds local optimum
- it always chooses the steps that provide immediate profit
- not that time- and space-consuming

**As a complex approach to the problem Genetic Algorithm was used since:**

- it gives higher range of solutions by evolving solutions within the algorithm run (mutation and crossover were used)
- it finds global optimum

## Implementation part:

#### Greedy algorithm:

```
def greedySolution(inters):
    solution = {}
    for intersection in inters:
        solution[intersection] = {}
        kopia = copy.deepcopy(inters[intersection].incoming)
        numpy.random.shuffle(kopia)
        for inc in kopia:
            solution[intersection][inc] = 1
    return solution
```

**Explanation:**

- Since the algorithm is greedy, it simply considers the first improvement, distributing 1 second for each incoming street of an intersection will already be enough for the algorithm to reach local optimum.

#### Genetic algorithm:

**Genetic algorithm consists of several parts:**

1. Initial population generator part

```
def createIndividual(inters):
    solution = {}
    for intersection in inters:
        solution[intersection] = {}
        kopia = copy.deepcopy(inters[intersection].incoming)
        numpy.random.shuffle(kopia)
        for inc in kopia:
            solution[intersection][inc] = 1
    return solution
    
popSize = 20
population = [list() for i in range(popSize)]
for i in range(popSize):
    if time.time() - start > 250:
        return population[0]
    individual = createIndividual(inters)
    population[i].append(individual)
    population[i].append(fitness(duration, cars, streets, individual, points, inters))
population = sorted(population, key=lambda x: x[1], reverse=True)
```

**Explanation:**

- The function above uses greedy approach to create an individual for its futher genetic evaluation
- Whereas, the loop is in charge of creating an initial population in form of a list of individuals and their fitness (which gets calculated by the heuristic function below)

2. Heuristic part (i.e., evaluation of a solution)

```
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
```

**Explanation:**

- Firstly, it creates a timetable for each intersection of the solution that is currently being processed. Timetable is a list of streets that are ordered in a way green lights have been distributed so far, e.g.: for a solution `On intersection I green light lasts 2 sec for the incoming street 1 and 1 sec for the other incoming street 2` the timetable will take a form `Inter I: [street 1, street 1, street 2]`
- Then, within each second of the simulation duration, it checks the current state of a car and proceeds it to the next step of its path according to such conditions of it as `driving time, queue position`
- This function is being called from the genetic algorithm function as

```
def fitness(duration, cars, streets, individual, points, inters): 
    return heuristic(duration, cars, streets, individual, points, inters)
```

3. Main evolution loop

```
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
```

**Explanation:**

- The stopping criterion of the population evolution is 5 current best individuals with no improvement or exceeded time restriction
- Firstly, a population individual gets chosen by tournament selection by the function, where the best individual out of mating pool is returned:

```
def tournament(population):
    matingPoolSize = 3
    matingPool = []
    for i in range(matingPoolSize):
        matingPool.append(population[random.randint(0, len(population) - 1)])
    matingPool = sorted(matingPool, key=lambda x: x[1], reverse=True)
    return matingPool[0][0]
```

- Then, this individual gets mutated by the function, where values of randomly selected individual intersection incoming streets get changed by a random number in the provided range:

```
def mutation(individual):
    for i in range(len(individual)//20 + 1):
        selectedInter = random.randint(0, len(individual) - 1)
        for street in individual[selectedInter]:
            individual[selectedInter][street] = random.randint(1, duration // len(individual[selectedInter]))
    return individual
```

- After that, two parents are selected by the same tournament function and get crossovered by the function, that returns the child of them that is formed by swapping their parts around randomly chosen cutting point (i.e., an intersection, in our case):

```
def crossOver(parent1, parent2):
    cuttingPoint = random.randint(0, len(parent1) - 1)
    part1 = {y: parent1[y] for y in range(cuttingPoint)}
    part2 = {y: parent2[y] for y in range(cuttingPoint, len(parent2))}
    child = {}
    child.update(part1)
    child.update(part2)
    return child
```

- Lastly, the updated with gotten children population gets sorted and rid of worst individuals in the amount of newly added individuals (in order to maintain population size stable)

## Conclusion

### Both algorithms indeed provide efficient solutions. The choice of an algorithm should be based on your goal: whether the solution is needed to be local or global and how fast you are willing to get solutions. Main points for this: Greedy algorithm - quickly found local optimum, Genetic - quite time-consuming but global optimum.

### Sources: 
#### No additional sources were used. Only our knowledge obtained during previous cources (e.g., Artificial Life and Cognitive Sciences, Algorithms and Data Structures)
