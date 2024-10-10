from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import math

def create_data_model(distance_matrix, depot):
    """Stores the data for the problem with the given depot."""
    data = {}
    n = len(distance_matrix)  # Number of teams
    # Set number of vehicles as an upper limit: ceil(n / 3) + 1
    data['num_vehicles'] = math.ceil(n / 3)
    data['depot'] = depot  # Set the current team as the depot
    data['distance_matrix'] = distance_matrix
    # Set demands: Depot has a demand of 0, others have a demand of 1
    
    #veh num no more than n
    # data['demands'] = [0 if i == depot else 1 for i in range(n)]
    

    # if force the vehicle num to be exactly n
    data['demands'] = [1] * n

    data['vehicle_capacities'] = [3] * data['num_vehicles']  # Each vehicle can visit up to 3 locations
    return data

def print_solution_custom(manager, routing, solution, data):
    """Prints solution in the customized format."""
    total_distance = 0
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(str(node_index+1))  # Use the team index for the route
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        
        # Only print if the vehicle has visited at least one location
        if len(route) > 1:
            route_output = ' -> '.join(route)  # Join the route elements
            print(f"{route_output}, distance: {route_distance}")
            total_distance += route_distance

    print(f"Total distance of all routes: {total_distance}\n")

def solve_vrp_for_each_team_as_depot(distance_matrix):
    """Solve the VRP for each team as the depot."""
    n = len(distance_matrix)  # Number of teams
    for depot in range(n):
        print(f"Depot: Team {depot + 1}")  # Print the depot in the correct format
        # Create data model for the current depot
        data = create_data_model(distance_matrix, depot)

        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        # Create Routing Model
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Capacity constraint
        def demand_callback(from_index):
            """Returns the demand of the node."""
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

         # Add this line to force using all vehicles
        # routing.SetFixedCostOfAllVehicles(1000)  # Arbitrary positive cost to force vehicle usage

        # Setting first solution heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution in the requested format
        if solution:
            print_solution_custom(manager, routing, solution, data)
        else:
            print(f"No solution found for depot: Team {depot + 1}\n")

# Example call with a given distance matrix
distance_matrix = [
    # [0, 745, 665, 929, 605, 521],
    # [745, 0, 80, 337, 1090, 315],
    # [665, 80, 0, 380, 1020, 257],
    # [929, 337, 380, 0, 1380, 408],
    # [605, 1090, 1020, 1380, 0, 1010],
    # [521, 315, 257, 408, 1010, 0]

    [0, 745, 665, 929],
    [745, 0, 80, 337],
    [665, 80, 0, 380],
    [929, 337, 380, 0]
]

if __name__ == "__main__":
    solve_vrp_for_each_team_as_depot(distance_matrix)





# from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# def create_data_model():
#     """Stores the data for the problem."""
#     data = {}
#     data['distance_matrix'] = [
#         [0, 745, 665, 929, 605, 521],
#         [745, 0, 80, 337, 1090, 315],
#         [665, 80, 0, 380, 1020, 257],
#         [929, 337, 380, 0, 1380, 408],
#         [605, 1090, 1020, 1380, 0, 1010],
#         [521, 315, 257, 408, 1010, 0],
#     ]
#     data['num_vehicles'] = 3  # At least 3 vehicles
#     data['depot'] = 0  # Start and end at the depot (home)
#     data['demands'] = [0, 1, 1, 1, 1, 1]  # Demand of each location, depot has 0 demand
#     data['vehicle_capacities'] = [3, 3, 3]  # Capacity of each vehicle
#     return data

# def print_solution(manager, routing, solution, data):
#     """Prints solution on console."""
#     total_distance = 0
#     total_load = 0
#     for vehicle_id in range(manager.GetNumberOfVehicles()):
#         index = routing.Start(vehicle_id)
#         route_distance = 0
#         route_load = 0
#         plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
#         while not routing.IsEnd(index):
#             node_index = manager.IndexToNode(index)
#             route_load += data['demands'][node_index]
#             plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#         plan_output += ' {0}\n'.format(manager.IndexToNode(index))
#         plan_output += 'Distance of the route: {}m\n'.format(route_distance)
#         plan_output += 'Load of the route: {}\n'.format(route_load)
#         print(plan_output)
#         total_distance += route_distance
#         total_load += route_load
#     print('Total distance of all routes: {}m'.format(total_distance))
#     print('Total load of all routes: {}'.format(total_load))

# def main():
#     """Solve the VRP problem with capacity constraints."""
#     # Instantiate the data problem.
#     data = create_data_model()

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['depot'])

#     # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def distance_callback(from_index, to_index):
#         # Returns the distance between the two nodes.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data['distance_matrix'][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add Capacity constraint.
#     def demand_callback(from_index):
#         """Returns the demand of the node."""
#         from_node = manager.IndexToNode(from_index)
#         return data['demands'][from_node]

#     demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
#     routing.AddDimensionWithVehicleCapacity(
#         demand_callback_index,
#         0,  # null capacity slack
#         data['vehicle_capacities'],  # vehicle maximum capacities
#         True,  # start cumul to zero
#         'Capacity')

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         print_solution(manager, routing, solution, data)
#     else:
#         print("No solution found.")

# if __name__ == '__main__':
#     main()
