import functions
from typing import List, Set, Tuple, Dict
import localSearch.greedy.greedyRandomized as greedy

def create_greedy_solution(customers: List[functions.Customer], vehicle_count, vehicle_capacity):
    vehicle_tours = [[]]*vehicle_count
    customers_pos = [0]*len(customers)
    remaining_customers = set(customers[1:])
    capacity_remaining = [vehicle_capacity]*vehicle_count

    for v in range(0, vehicle_count):
        capacity_remaining[v] = vehicle_capacity
        vehicle_tours[v] = [customers[0]]

        while sum([capacity_remaining[v] >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            nearestCustomer = None
            minlength = 0
            for customer in remaining_customers:
                if capacity_remaining[v] >= customer.demand:
                    l = functions.length(vehicle_tours[v][-1], customer)
                    if(minlength == 0 or minlength > l): 
                        minlength = l
                        nearestCustomer = customer
            capacity_remaining[v] -= nearestCustomer.demand
            vehicle_tours[v].append(nearestCustomer)
            used.add(nearestCustomer)
            customers_pos[nearestCustomer.index] = {"vehicle_id":v, "position":len(vehicle_tours[v])-1}
            remaining_customers -= used
    for vehicle_tour in vehicle_tours: vehicle_tour.append(customers[0])
    if len(remaining_customers) > 0: return greedy.create_greedy_randomized_solution(customers, vehicle_count, vehicle_capacity)
    return (vehicle_tours, customers_pos, capacity_remaining)