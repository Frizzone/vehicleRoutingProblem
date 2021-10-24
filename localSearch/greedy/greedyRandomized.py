import functions
from typing import List, Set, Tuple, Dict
import random, math

def create_greedy_randomized_solution(customers: List[functions.Customer], vehicle_count, vehicle_capacity):
    vehicle_tours = [[]]*vehicle_count
    customers_pos = [0]*len(customers)
    remaining_customers = set(customers[1:])
    capacity_remaining = [0]*vehicle_count
    is_vehicle_full = [False]*vehicle_count

    for v_id in range(0, vehicle_count):
        capacity_remaining[v_id] = vehicle_capacity
        vehicle_tours[v_id] = [customers[0]]

    while not all(is_vehicle_full):
        v_id = None
        while v_id==None or (is_vehicle_full[v_id]): v_id = random.randint(0, vehicle_count-1)
        used = set()
        alfa = random.random()/5 #alfa 0%-20%
        size = math.ceil(alfa*len(customers))
        last_customer = vehicle_tours[v_id][-1]
        bestCandidatesList = selectBestCandidates(v_id, last_customer, remaining_customers, capacity_remaining, size)
        if len(bestCandidatesList) > 0:
            bestCustomer = random.choice(bestCandidatesList)
            capacity_remaining[v_id] -= bestCustomer.demand
            vehicle_tours[v_id].append(bestCustomer)
            customers_pos[bestCustomer.index] = {"vehicle_id":v_id, "position":len(vehicle_tours[v_id])-1}
            used.add(bestCustomer)
            remaining_customers -= used
        is_vehicle_full[v_id] = not (sum([capacity_remaining[v_id] >= customer.demand for customer in remaining_customers]) > 0)

    for vehicle_tour in vehicle_tours: vehicle_tour.append(customers[0])
    if len(remaining_customers) > 0: return create_greedy_randomized_solution(customers, vehicle_count, vehicle_capacity)
    else: return (vehicle_tours, customers_pos, capacity_remaining)

def selectBestCandidates(v_id, customer, remaining_customers, capacity_remaining, size):
    bestCustomers = []
    for c in remaining_customers:
        if(customer != c and capacity_remaining[v_id] >= c.demand):
            l = functions.length(customer, c)
            bestCustomers.append((c, l))
    bestCustomers.sort(key=lambda x:x[1], reverse=False)
    
    bestCandidatesList = []
    for c in bestCustomers:
        bestCandidatesList.append(c[0])
        if(len(bestCandidatesList)>=size): return bestCandidatesList
    return bestCandidatesList

def create_random_solution(customers: List[functions.Customer], vehicle_count, vehicle_capacity):
    vehicle_tours = [None]*vehicle_count
    customers_pos = [0]*len(customers)
    remaining_customers = set(customers[1:])
    capacity_remaining = [vehicle_capacity]*vehicle_count

    for v_id in range(0, vehicle_count):
        vehicle_tours[v_id] = [customers[0]]
        while sum([capacity_remaining[v_id] >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            shuffled_customers = list(remaining_customers)
            random.shuffle(shuffled_customers)
            for customer in shuffled_customers:
                if capacity_remaining[v_id] >= customer.demand:
                    capacity_remaining[v_id] -= customer.demand
                    vehicle_tours[v_id].append(customer)
                    customers_pos[customer.index] = {"vehicle_id":v_id, "position":len(vehicle_tours[v_id])-1}
                    used.add(customer)
            remaining_customers -= used
                
    for vehicle_tour in vehicle_tours: vehicle_tour.append(customers[0])
    return (vehicle_tours, customers_pos, capacity_remaining)
