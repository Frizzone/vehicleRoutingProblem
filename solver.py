#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import functions
import mixIntegerProgram.vpr_mip_gurobi as vpr_mip_gurobi
import geneticAlgorithm.geneticAlgorithm as vpr_ga
import visualization
import localSearch.MH.iteratedLocalSearchMH as ils
import localSearch.MH.graspMH as grasp
import localSearch.localSearch as ls
import cProfile, pstats
import io

__PLOT = False

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(functions.Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0]

    option = input ("(1) MIP - Gurobi Solver\n(2) Genetic Algorithm\n(3) ILS MH\n(4) Grasp MH\n>>")

    if(option == "1"):
        vehicle_tours = vpr_mip_gurobi.vpr_mip_gurobi(customers, vehicle_count, vehicle_capacity)
    if(option == "2"):
        popsize=100
        elitesize=10
        mutationRate=0.1
        generations=200
        
        inp = input("Population Size (default = 100):")
        if(inp != ""): popsize = int(inp)
        
        inp = input("Elite Size (default = 10):")
        if(inp != ""): elitesize = int(inp)
        
        inp = input("Mutation Rate (default = 0.1):")
        if(inp != ""): mutationRate = float(inp)
        
        inp = input("Number of Generations (default = 200):")
        if(inp != ""): generations = int(inp)

        vehicle_tours = vpr_ga.vpr_geneticAlgorithm(customers=customers, vehicle_count=vehicle_count, vehicle_capacity=vehicle_capacity, popSize=popsize, eliteSize=elitesize, mutationRate=mutationRate, generations=generations)

    if(option == "3"):
        timeout = int(input("Timeout in seconds:"))
        vehicle_tours = ils.iterated_local_search(customers, vehicle_count, vehicle_capacity, timeout)
    if(option == "4"):
        timeout = int(input("Timeout in seconds:"))
        vehicle_tours = grasp.grasp_mh(customers, vehicle_count, vehicle_capacity, timeout)

    if(__PLOT): visualization.DrawNetwork(vehicle_tours, customers, vehicle_count)
    # calculate the cost of the solution; for each vehicle the length of the route
    
    obj = functions.tourLen(vehicle_tours, vehicle_count, depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + '0' + '\n'
    for v in range(0, vehicle_count):
        #outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'
        outputData += ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + '\n'

    
    return outputData

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            
            #profiler = cProfile.Profile()
            #profiler.enable()
            print(solve_it(input_data))
            #profiler.disable()
            #stats = pstats.Stats(profiler).sort_stats('ncalls')
            #stats = pstats.Stats(profiler).strip_dirs().sort_stats('ncalls')

            #result = io.StringIO()
            #stats = pstats.Stats(profiler, stream = result).sort_stats('ncalls')
            #stats.print_stats()
            #result = result.getvalue()

            #export data
            #stats = pstats.Stats(profiler)
            #stats.dump_stats('export-data')

            # Chop the string into a csv-like buffer
            #result = 'ncalls' + result.split('ncalls')[-1]
            #result = '\n'.join([','.join(line.rstrip().split(None, 6)) for line in result.split('\n')])

            # Save it into disk
            #with open('cProfileExport1.csv', 'w+') as f:
            #    f.write(result)


        
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

