import functions
from localSearch.solution import Solution

def realocate(solution: Solution, c1: functions.Customer, c2:functions.Customer, only_improvements=True):
    v1_id = solution.customers_pos[c1.index]["vehicle_id"]
    v2_id = solution.customers_pos[c2.index]["vehicle_id"]
    if(v1_id == v2_id):  improvement = inner_realocate(solution, v1_id, c1, c2, only_improvements)
    elif(v1_id != v2_id): improvement = outer_realocate(solution, v1_id, c1, v2_id, c2, only_improvements)
    return improvement


# 0->1->2->3->4---->5
# 0---->2->3->4->1->5
def inner_realocate(solution: Solution, v_id, c1, c2, only_improvements=True):
    posc1 = solution.customers_pos[c1.index]["position"]
    posc2 = solution.customers_pos[c2.index]["position"]
    if not only_improvements or is_inner_realocate_improvement(solution, v_id, posc1, posc2):
        do_inner_realocate(solution, v_id, posc1, posc2)
        return True
    else:
        return False

def do_inner_realocate(solution: Solution, v_id, posc1, posc2):
    route = solution.vehicle_routes[v_id]    
    a=min([posc1,posc2])
    b=max([posc1,posc2])
    item = route[a]
    route[a:b] = route[a+1:b+1]
    route[b] = item
    solution.rebuild_customer_indexes(v_id)

# swap (V_ID, 1,4)
#0->1 + 1->2 + 4->5 greater than 0->2 + 4->1 + 1->5
def is_inner_realocate_improvement(solution: Solution, v_id, i, j):
    tour = solution.vehicle_routes[v_id]
    a=min([i,j])
    b=max([i,j])
    actual = functions.length(tour[a-1], tour[a]) + functions.length(tour[a], tour[a+1]) + functions.length(tour[b], tour[b+1])
    new = functions.length(tour[a-1], tour[a+1]) + functions.length(tour[b], tour[a]) + functions.length(tour[a], tour[b+1])
    return new < actual

def outer_realocate(solution: Solution, v1_id, c1, v2_id, c2, only_improvements=True):
    posc1 = solution.customers_pos[c1.index]["position"]
    posc2 = solution.customers_pos[c2.index]["position"]
    if is_feasible_realocate(solution, v1_id, v2_id, c1, c2) and (not only_improvements or is_outer_swap_improvement(posc1, posc2, solution.vehicle_routes[v1_id], solution.vehicle_routes[v2_id])): 
        do_outer_realocate(solution, v1_id, posc1, c1, v2_id, posc2, c2)
        return True
    else: 
        return False

def do_outer_realocate(solution: Solution, v1_id, posc1, c1, v2_id, posc2, c2):
    solution.vehicle_routes[v1_id].pop(posc1)
    solution.vehicle_routes[v2_id].insert(posc2+1, c1)
    solution.vehicle_capacities[v1_id] = solution.vehicle_capacities[v1_id] + c1.demand
    solution.vehicle_capacities[v2_id] = solution.vehicle_capacities[v2_id] - c1.demand
    solution.rebuild_customer_indexes(v1_id)
    solution.rebuild_customer_indexes(v2_id)

def is_outer_swap_improvement(i, j, tour1, tour2):
    actualr1 = functions.length(tour1[i-1], tour1[i]) +  functions.length(tour1[i], tour1[i+1])
    actualr2 = functions.length(tour2[j-1], tour2[j]) +  functions.length(tour2[j], tour2[j+1])
    newr1 = functions.length(tour1[i-1], tour1[i+1])
    newr2 = functions.length(tour2[j-1], tour2[j]) + functions.length(tour2[j], tour1[i]) + functions.length(tour1[i], tour2[j+1])
    return  (newr1 + newr2) < (actualr1 + actualr2)

def is_feasible_realocate(solution, v1_id, v2_id, c1, c2):
        k1 = solution.vehicle_capacities[v1_id] + c1.demand
        k2 = solution.vehicle_capacities[v2_id] - c1.demand
        if(k1 < 0 or k2 < 0 ): return False
        else: return True