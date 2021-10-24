import functions
from typing import List
import time
import localSearch.localSearch as ls
import localSearch.greedy.greedyRandomized as greedy
import copy

def grasp_mh(customers: List[functions.Customer], vehicle_count, vehicle_capacity, timeout):
    bestl = None
    bestSolution = None
    timeout = time.time() + timeout
    while True:
        (vehicle_routes, customers_pos, capacity_remaining) = greedy.create_greedy_randomized_solution(customers, vehicle_count, vehicle_capacity)
        solution = ls.Solution(vehicle_routes, customers_pos, capacity_remaining)
        ls.local_search_first_improvement(solution, customers)
        l = functions.tourLen(solution.vehicle_routes, len(solution.vehicle_routes), customers[0])
        if(bestl == None or l < bestl):
            bestl = l
            bestSolution = copy.deepcopy(solution.vehicle_routes)
            print(l)
        if time.time() > timeout: break
    return bestSolution