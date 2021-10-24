import random, operator, matplotlib.pyplot as plt
import functions
from typing import List, Set, Tuple, Dict
import localSearch.localSearch as ls
import localSearch.operations.swap as swap
import localSearch.operations.realocate as realocate
import localSearch.greedy.greedyRandomized as greedy
from localSearch.solution import Solution
from collections import namedtuple
import time

_PLOT_PROGRESS = True
Input = namedtuple("Input", ['Customers', 'VehicleCount', 'VehicleCapacity', "Depot"])

def vpr_geneticAlgorithm(customers, vehicle_count, vehicle_capacity, popSize, eliteSize, mutationRate, generations):
    input = Input(customers, vehicle_count, vehicle_capacity, customers[0])
    population = initial_population(popSize, input)
    progress = []
    
    initial_time = time.time()
    for i in range(0, generations):
        population = nextGeneration(population, eliteSize, mutationRate, input)
        if(_PLOT_PROGRESS): 
            p = best_individual(population, input).distance
            if(len(progress) > 0 and p < progress[-1]): 
                print(str(i) + " - "+ str(p) + " - " + str((time.time() - initial_time)/(i+1)))
            progress.append(p)

    if(_PLOT_PROGRESS):  
        plt.plot(progress)
        plt.show()
    
    ls.local_search_first_improvement(population[0], input.Customers)
    return population[0].vehicle_routes

#Initial population
def initial_population(popSize, input: Input):
    population = []

    i=0
    while (i<= popSize):
        (vehicle_routes, customers_pos, capacity_remaining) = greedy.create_random_solution(input.Customers, input.VehicleCount, input.VehicleCapacity)
        solution = Solution(vehicle_routes, customers_pos, capacity_remaining)
        population.append(solution)
        i = i+1

    for individual in population: individual.calculate_distance(input.Depot)    
    return population


def nextGeneration(currentGen: List[Solution], eliteSize, mutationRate, input: Input):
    orderedPopulation = order_population(currentGen, input)
    children = breed_population(orderedPopulation, eliteSize, input)
    nextGeneration = mutate_population(children, mutationRate, input)
    return nextGeneration

#Order population
def order_population(population: List[Solution], input: Input):
    populationRanked = {}
    for i in range(0,len(population)):
        populationRanked[i] = population[i].distance
    populationRanked = sorted(populationRanked.items(), key = operator.itemgetter(1), reverse = False)
    orderedPopulation = []

    for i in range(0, len(populationRanked)):
        index = populationRanked[i][0]
        orderedPopulation.append(population[index])
    return orderedPopulation

#Best Distance
def best_individual(population: List[Solution], input: Input):
    populationRanked = {}
    for i in range(0,len(population)): 
        populationRanked[i] = population[i].distance
    populationRanked = sorted(populationRanked.items(), key = operator.itemgetter(1), reverse = False)
    index = populationRanked[0][0]
    return population[index]

# breed Population and create a children population modified
def breed_population(matingpool: List[Solution], eliteSize, input: Input):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))
    

    # the elite bests (elite) individuals (routes) in matingpool don't suffer crossover modification
    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    # the remaining worst: breed with random individuals (routes) in matingpool and create modified children
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1], input)
        children.append(child)

    return children

#breed
#firts: get best route of the parents
#second: get elements of the parent route, if already added get the nearest customer
def breed(parent1: Solution, parent2: Solution, input: Input):
    child = Solution([None]*input.VehicleCount, [0]*len(input.Customers), [input.VehicleCapacity]*input.VehicleCount)
    remaining_customers = set(input.Customers[1:])
    used = set()

    #get the best tour from parents
    bestTour = functions.best_tour(parent1.vehicle_routes + parent2.vehicle_routes, input.Depot)
    for c in bestTour: 
        if(c.index!=0 and (child.vehicle_capacities[0] - c.demand) >= 0): 
            child.add_item(0, c, input.Depot)
            used.add(c)
    child.add_item(0,  input.Depot,  input.Depot)
    remaining_customers -= used

    #merge others routes
    for vehicle_id in range(1, input.VehicleCount):
        child.add_item(vehicle_id, input.Depot, input.Depot)
        parent=random.choice([parent1, parent2])
        for c in parent.vehicle_routes[vehicle_id]:
            used = set()
            if(c.index != 0 and len(remaining_customers)>0): 
                if(c in remaining_customers and (child.vehicle_capacities[vehicle_id] - c.demand) >= 0):
                    child.add_item(vehicle_id, c, input.Depot)
                    used.add(c)
                    remaining_customers -= used
                else:
                    nearest_customer = functions.nearest_node(remaining_customers, child.vehicle_routes[vehicle_id][-1], child.vehicle_capacities[vehicle_id])
                    if(nearest_customer != None and (child.vehicle_capacities[vehicle_id] - c.demand) >= 0):
                        child.add_item(vehicle_id, nearest_customer, input.Depot)
                        used.add(nearest_customer)
                        remaining_customers -= used
        while sum([child.vehicle_capacities[vehicle_id] >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            nearest_customer = functions.nearest_node(remaining_customers, child.vehicle_routes[vehicle_id][-1], child.vehicle_capacities[vehicle_id])
            if ((child.vehicle_capacities[vehicle_id] - nearest_customer.demand) >= 0):
                child.add_item(vehicle_id, nearest_customer, input.Depot)
                used.add(nearest_customer)
                remaining_customers -= used             
        child.add_item(vehicle_id, input.Depot, input.Depot)

    if(len(remaining_customers) > 0):
        (vehicle_routes, customers_pos, capacity_remaining) = greedy.create_random_solution(input.Customers, input.VehicleCount, input.VehicleCapacity)
        child = ls.Solution(vehicle_routes, customers_pos, capacity_remaining)

    child.calculate_distance(input.Depot)
    return child
        

#for each individual in population 
    # for each gene
        # with a probability "mutationRate" swap the gene with a random gene
def mutate_population(population, mutationRate, input):
    mutatedPopulation = []
    orderedPopulation = order_population(population, input)
    i=0
    for individual in orderedPopulation:
        if(i==0): mutatedPopulation.append(individual)
        else:
            mutate(individual, input, mutationRate)
            mutatedPopulation.append(individual)
        i=i+1
    return mutatedPopulation

def mutate(individual: Solution, input: Input, mutationRate):
    customers_without_depot = input.Customers[1:-1]
    random.shuffle(customers_without_depot)
    improvement = False
    for c1 in customers_without_depot:
        if(random.random() < mutationRate):
            for c2 in customers_without_depot:
                if(c1.index!=c2.index): 
                    if(swap.swap(individual, c1, c2, only_improvements=True)): 
                        improvement = True
                        break
                    if(realocate.realocate(individual, c1, c2, only_improvements=True)):
                        improvement = True
                        break
    if (improvement): individual.calculate_distance(input.Depot)