import functions
import random
import localSearch.operations.swap as swap
import localSearch.operations.realocate as realocate
from typing import List
from localSearch.solution import Solution
from itertools import permutations

def local_search_first_improvement(solution: Solution, customers: List[functions.Customer]):
    neighborhood = generate_neighborhood(customers)
    finish = False

    while (not finish):
        finish = True
        random.shuffle(neighborhood)
        for neighbor in neighborhood:
            if(valid_neighbor(neighbor)): 
                if(swap.swap(solution, neighbor[0], neighbor[1], only_improvements=True)): 
                    finish = False
                    break
                if(realocate.realocate(solution, neighbor[0], neighbor[1], only_improvements=True)):
                    finish = False
                    break

def valid_neighbor(neighbor):
    return (neighbor[0].index!=neighbor[1].index and (neighbor[0].index !=0 and neighbor[1].index !=0))

def generate_neighborhood(customers: List[functions.Customer]):
    neighborhood = permutations(customers, 2)
    return list(neighborhood)
