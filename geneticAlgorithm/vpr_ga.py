import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, math
import functions
import geneticAlgorithm.individual as ind
from typing import List, Set, Tuple, Dict

_PLOT_PROGRESS = True

def vpr_geneticAlgorithm(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    population = initialPopulation(popSize, customers, vehicle_count, vehicle_capacity)
    progress = []
    if(_PLOT_PROGRESS): 
        p = bestIndividual(population).distance
        progress.append(p)
    
    for i in range(0, generations):
        population = nextGeneration(population, eliteSize, mutationRate)
        if(_PLOT_PROGRESS): 
            p = bestIndividual(population).distance
            print(p)
            progress.append(p)

    if(_PLOT_PROGRESS):  
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
    
    vehicle_tours = population[0].vehicle_tours
    population[0].testConstraints("Teste Final")
    return vehicle_tours

#Initial population
def initialPopulation(popSize, customers, vehicle_count, vehicle_capacity):
    population = []

    i=0
    while (i<= popSize):
        tours = functions.createRandomTours(customers, vehicle_count, vehicle_capacity)
        if (tours != None):
            population.append(tours)
            i = i+1
        
    return population

def nextGeneration(currentGen, eliteSize, mutationRate):
    orderedPopulation = orderPopulation(currentGen)
    children = breedPopulation(orderedPopulation, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

#Order population
def orderPopulation(population: List[ind.Individual]):
    populationRanked = {}
    for i in range(0,len(population)):
        populationRanked[i] = population[i].routeDistance()
    populationRanked = sorted(populationRanked.items(), key = operator.itemgetter(1), reverse = False)
    orderedPopulation = []

    for i in range(0, len(populationRanked)):
        index = populationRanked[i][0]
        orderedPopulation.append(population[index])
    return orderedPopulation

#Best Distance
def bestIndividual(population: List[ind.Individual]):
    populationRanked = {}
    for i in range(0,len(population)):
        populationRanked[i] = population[i].routeDistance()
    populationRanked = sorted(populationRanked.items(), key = operator.itemgetter(1), reverse = False)
    index = populationRanked[0][0]
    return population[index]

# breed Population and create a children population modified
def breedPopulation(matingpool: List[ind.Individual], eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    # the elite bests (elite) individuals (routes) in matingpool don't suffer crossover modification
    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    # the remaining worst: breed with random individuals (routes) in matingpool and create modified children
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
        
    return children

#breed
#firts: get best route of the parents
#second: get elements of the parent route, if already added get the nearest customer
def breed(parent1: ind.Individual, parent2: ind.Individual):
    child = ind.Individual(parent1.customers, parent1.vehicle_count, parent1.vehicle_capacity)
        
    #get the best tour from parents
    (bestTour, bestLen) = functions.bestTour(parent1.vehicle_tours + parent2.vehicle_tours, parent1.customers[0])
    for c in bestTour: 
        if(c.index!=0): 
            child.addItemRoute(0, c)
    child.addItemRoute(0, parent1.customers[0])
    
    for vehicle_id in range(1, parent1.vehicle_count):
        randomParent = random.randint(0, 1)
        if(randomParent==0):
            breedRouteToChild(parent1, child, vehicle_id)
        else:
            breedRouteToChild(parent2, child, vehicle_id)
    
    if(min(child.selected) == 0): 
        return parent1
    return child

#get a route, repeated customers will be replaced by the nearest customer
def breedRouteToChild(parent, child, vehicle_id):
    randomTour = int(random.random() * len(parent.vehicle_tours))
    for c in parent.vehicle_tours[randomTour]:
        if(c.index !=0 and child.selected[c.index]==0):
            child.addItemRoute(vehicle_id, c)
        else:
            c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
            if(c != None): child.addItemRoute(vehicle_id, c)
    
    finish = False        
    while(not finish):
        c = functions.nearestNode(parent.customers, child.vehicle_tours[vehicle_id][-1], child.selected)
        if(c == None): finish = True
        else: finish = not (child.addItemRoute(vehicle_id, c))
    
    child.addItemRoute(vehicle_id, child.customers[0])
        

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutatePopulation(population, mutationRate):
    mutatedPopulation = []
    orderedPopulation = orderPopulation(population)
    i=0
    for ind in orderedPopulation:
        if(i==0): mutatedPopulation.append(ind)
        else:
            mutatedInd = mutate(ind, mutationRate)
            mutatedPopulation.append(mutatedInd)
        i=i+1
    return mutatedPopulation

def mutate(individual, mutationRate):
    for swappedK in range(1, len(individual.vehicle_tours)):
        for swappedC in range(1, len(individual.vehicle_tours[swappedK])-1):
            if(random.random() < mutationRate):
                individual.outerSwap(swappedK, swappedC)
            if(random.random() < mutationRate):
                individual.innerSwap(swappedK, swappedC)
    return individual