import math
from collections import namedtuple
import random

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

# calculate the cost of the solution; for each vehicle the length of the route
def tourLen(vehicle_tours, vehicle_count, depot):
    obj = 0
    for v in range(0, vehicle_count):
        if len(vehicle_tours[v]) > 0: obj += routeLen(vehicle_tours[v], depot)
    return obj

# calculate the cost of the solution; for each vehicle the length of the route
def routeLen(vehicle_route, depot):
    obj = 0
    obj += length(depot,vehicle_route[0])
    for i in range(0, len(vehicle_route)-1):
        obj += length(vehicle_route[i],vehicle_route[i+1])
    obj += length(vehicle_route[-1],depot)
    return obj

def bestTour(vehicle_tours, depot):
    minTour = vehicle_tours[0]
    minlen = routeLen(vehicle_tours[0], depot)
    for i in range (1, len(vehicle_tours)):
        actuallen = routeLen(vehicle_tours[i], depot)
        if(actuallen<minlen): 
            minlen = actuallen
            minTour = vehicle_tours[i]
    return (minTour, minlen)

# calculate the capacity per distance unit
def route_capacity_per_distance(vehicle_route, depot):
    leng = 0
    cap = 0
    leng += length(depot,vehicle_route[0])
    for i in range(0, len(vehicle_route)-1):
        leng += length(vehicle_route[i],vehicle_route[i+1])
        cap += vehicle_route[i].demand
    leng += length(vehicle_route[-1],depot)
    return (cap/leng)

def best_tour(vehicle_tours, depot):
    best_tour = vehicle_tours[0]
    capacity_per_distance_best = route_capacity_per_distance(vehicle_tours[0], depot)
    for i in range (1, len(vehicle_tours)):
        capacity_per_distance = routeLen(vehicle_tours[i], depot)
        if(capacity_per_distance_best<capacity_per_distance): 
            capacity_per_distance_best = capacity_per_distance
            best_tour = vehicle_tours[i]
    return best_tour

def nearestNode(customers, customer, selected):
    nearestNode = 0
    minlength = 0
    for j in range(len(customers)):
        if(selected[customers[j].index] == 0 and customers[j].index != 0):
            l = length(customer, customers[j])
            if(minlength == 0 or minlength > l): 
                minlength = l
                nearestNode = j
    if nearestNode!=0: return customers[nearestNode]
    else: return None

def nearest_node(remaining_customers, customer, capacity_remaining):
    nearestCustomer = None
    minlength = 0
    for next_customer in remaining_customers:
        if capacity_remaining >= next_customer.demand:
            l = length(customer, next_customer)
            if(nearestCustomer == None or minlength > l): 
                minlength = l
                nearestCustomer = next_customer
    return nearestCustomer
    
def randomizedNearestNode(customers, customer, selected):
    bestCandidatesOrdered = []
    customer_count = len(customers)
    for i in range(customer_count):
        if(selected[customers[i].index] == 0 and customers[i].index != 0):
            l = length(customer, customers[i])
            bestCandidatesOrdered.append((customers[i], l))
    bestCandidatesOrdered.sort(key=lambda x:x[1], reverse=False)

    #alfa 0%-20%
    alfa = random.random()/5
    size = math.ceil(alfa*len(bestCandidatesOrdered))
    if(size > len(bestCandidatesOrdered)): size = len(bestCandidatesOrdered)
    if(size == 0): return None
    return random.choice(bestCandidatesOrdered[0:size])[0]