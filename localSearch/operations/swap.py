import functions
from localSearch.solution import Solution

def swap(solution: Solution, c1: functions.Customer, c2:functions.Customer, only_improvements=True):
    v1_id = solution.customers_pos[c1.index]["vehicle_id"]
    v2_id = solution.customers_pos[c2.index]["vehicle_id"]
    if(v1_id == v2_id):  improvement = inner_swap(solution, v1_id, c1, c2, only_improvements)
    elif(v1_id != v2_id): improvement = outer_swap(solution, v1_id, c1, v2_id, c2, only_improvements)
    return improvement

# swap (V_ID, B,E)
# A->B->C->D->E->F
# A->E->D->C->B->F (A-> reverve(B->C->D->E) ->F)
def inner_swap(solution: Solution, v_id, c1, c2, only_improvements=True):
    posc1 = solution.customers_pos[c1.index]["position"]
    posc2 = solution.customers_pos[c2.index]["position"]
    if not only_improvements or is_inner_swap_improvement(solution, v_id, posc1, posc2): 
        do_inner_swap(solution, v_id, posc1, posc2)
        return True
    else: 
        return False

def do_inner_swap(solution: Solution, v_id, posc1, posc2):
    a=min([posc1,posc2])
    b=max([posc1,posc2])
    solution.vehicle_routes[v_id][a:b+1] = reversed(solution.vehicle_routes[v_id][a:b+1])
    solution.rebuild_customer_indexes(v_id)

def is_inner_swap_improvement(solution: Solution, v_id, i, j):
    a=min([i,j])
    b=max([i,j])
    tour = solution.vehicle_routes[v_id]
    actual = functions.length(tour[a-1], tour[a]) +  functions.length(tour[b], tour[b+1])
    new = functions.length(tour[a-1], tour[b]) +  functions.length(tour[a], tour[b+1])
    return new < actual

#outer swap
def outer_swap(solution: Solution, v1_id, c1, v2_id, c2, only_improvements=True):
    posc1 = solution.customers_pos[c1.index]["position"]
    posc2 = solution.customers_pos[c2.index]["position"]
    if is_feasible_swap(solution, v1_id, v2_id, c1, c2) and (not only_improvements or is_outer_swap_improvement(posc1, posc2, solution.vehicle_routes[v1_id], solution.vehicle_routes[v2_id])): 
        do_outer_swap(solution, v1_id, posc1, c1, v2_id, posc2, c2)
        return True
    else: return False

def do_outer_swap(solution: Solution, v1_id, posc1, c1, v2_id, posc2, c2):
    solution.vehicle_routes[v1_id][posc1] = c2
    solution.vehicle_routes[v2_id][posc2] = c1
    solution.customers_pos[c1.index]["vehicle_id"] = v2_id
    solution.customers_pos[c1.index]["position"] = posc2
    solution.customers_pos[c2.index]["vehicle_id"] = v1_id
    solution.customers_pos[c2.index]["position"] = posc1
    solution.vehicle_capacities[v1_id] = solution.vehicle_capacities[v1_id] - c2.demand + c1.demand
    solution.vehicle_capacities[v2_id] = solution.vehicle_capacities[v2_id] - c1.demand + c2.demand
    
def is_outer_swap_improvement(i, j, tour1, tour2):
    actualr1 = functions.length(tour1[i-1], tour1[i]) +  functions.length(tour1[i], tour1[i+1])
    actualr2 = functions.length(tour2[j-1], tour2[j]) +  functions.length(tour2[j], tour2[j+1])
    newr1 = functions.length(tour1[i-1], tour2[j]) +  functions.length(tour2[j], tour1[i+1])
    newr2 = functions.length(tour2[j-1], tour1[i]) +  functions.length(tour1[i], tour2[j+1])
    return  (newr2 + newr1) < (actualr1 + actualr2)

def is_feasible_swap(solution, v1_id, v2_id, c1, c2):
        k1 = solution.vehicle_capacities[v1_id] - c2.demand + c1.demand
        k2 = solution.vehicle_capacities[v2_id] - c1.demand + c2.demand
        if(k1 < 0 or k2 < 0 ): return False
        else: return True