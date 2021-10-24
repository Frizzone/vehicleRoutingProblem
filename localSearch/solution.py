import functions

class Solution:
    def __init__(self, vehicle_routes, customers_pos, vehicle_capacities):
        self.vehicle_routes = vehicle_routes
        self.customers_pos = customers_pos
        self.vehicle_capacities = vehicle_capacities
        self.distance = 0

    def add_item(self, vehicle_id, customer, depot):
        if(self.vehicle_capacities[vehicle_id] - customer.demand >= 0): 
            if(self.vehicle_routes[vehicle_id] == None): self.vehicle_routes[vehicle_id] = [depot]
            self.vehicle_capacities[vehicle_id] -= customer.demand
            self.vehicle_routes[vehicle_id].append(customer)
            self.customers_pos[customer.index] = {"vehicle_id":vehicle_id, "position":len(self.vehicle_routes[vehicle_id])-1}
        else: 
            raise Exception('There is no capacity in the vehicle')
    
    def calculate_distance(self, depot):
        self.distance = functions.tourLen(self.vehicle_routes, len(self.vehicle_routes), depot)
        return self.distance

    def rebuild_customer_indexes(self, vehicle_id):
        pos = 0
        for customer in self.vehicle_routes[vehicle_id]: 
            if(customer.index != 0): 
                self.customers_pos[customer.index]["vehicle_id"] = vehicle_id
                self.customers_pos[customer.index]["position"] = pos
            pos+=1
        return True