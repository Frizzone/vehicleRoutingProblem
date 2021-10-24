import functions
from typing import List
import random
import time
import localSearch.localSearch as ls
import localSearch.operations.swap as swap
import localSearch.operations.realocate as realocate
import localSearch.greedy.greedy as greedy
import copy

def iterated_local_search(customers: List[functions.Customer], vehicle_count, vehicle_capacity, timeout):
    (vehicle_routes, customers_pos, capacity_remaining) = greedy.create_greedy_solution(customers, vehicle_count, vehicle_capacity)
    solution = ls.Solution(vehicle_routes, customers_pos, capacity_remaining)
    ls.local_search_first_improvement(solution, customers)
 
    l = functions.tourLen(solution.vehicle_routes, len(solution.vehicle_routes), customers[0])
    bestl = l
    bestSolution = copy.deepcopy(solution.vehicle_routes)

    timeout = time.time() + timeout
    while True:

        pertubation(solution, customers)
        ls.local_search_first_improvement(solution, customers)
        l = functions.tourLen(solution.vehicle_routes, len(solution.vehicle_routes), customers[0])

        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = copy.deepcopy(solution.vehicle_routes)
            print(l)

        if time.time() > timeout: break    
    
    return bestSolution

def pertubation(solution: ls.Solution, customers: List[functions.Customer]):
    customers_without_depot = customers[1:-1]

    for i in range (0,3):
        c1 = random.choice(customers_without_depot)
        c2 = random.choice(customers_without_depot)
        if(c1 != c2): 
            operation = random.choice([0,1])
            if(operation == 0): swap.swap(solution, c1, c2, only_improvements=False)
            elif(operation == 1): realocate.realocate(solution, c1, c2, only_improvements=False)
    