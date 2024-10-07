from ini_sche import generate_team_centric_schedule
from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *


import random
import copy
import time
import sys
from collections import deque

def tabu_search(schedule, heuristic_func, max_idle_iterations=5000, max_idle_rounds=1000):
    num_teams = len(schedule)
    
    # Initialize the tabu list as a dictionary with a fixed max size of n
    tabu_list = {}  # Dictionary to store tabu moves with their iteration expiration
    tabu_order = []  # List to track the order of moves in the tabu list for removing the oldest one
    
    iteration = 0   # Keep track of the iteration number
    best_schedule = copy.deepcopy(schedule)  # Global best solution
    current_schedule = copy.deepcopy(schedule)  # The current solution being explored
    best_cost = heuristic_func(best_schedule)
    
    idle_iterations = 0  # Counter for idle iterations (no local improvement)
    idle_rounds = 0  # Counter for idle rounds (no global improvement)
    
    while idle_iterations < max_idle_iterations and idle_rounds < max_idle_rounds:

        current_best_schedule = None
        current_best_cost = float('inf')
        best_move = None  # Will hold the best move (k, idx1, idx2)
        
        # Loop through the selected neighborhood operations (k = 0, 1, 2)
        for k in range(3):  # Only considering k = 0, k = 1, k = 2

            if k == 1 or k == 2:
                # Swap home or swap team (2 indices needed)
                for idx1 in range(num_teams):
                    for idx2 in range(idx1 + 1, num_teams):
                        
                        if k == 1:
                            # Swap home
                            new_schedule = swap_home(copy.deepcopy(current_schedule), idx1, idx2)
                        if k == 2:
                            # Swap team
                            new_schedule = swap_team(copy.deepcopy(current_schedule), idx1, idx2)

                        # Check if the resulting schedule is feasible
                        if count_violations(new_schedule) > 0:
                            continue  # Skip if the new schedule has violations

                        new_cost = heuristic_func(new_schedule)

                        # Aspiration criterion: Accept tabu move if it improves global best
                        if (k, idx1, idx2) in tabu_list:
                            if new_cost < best_cost:  # Aspiration criterion
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost
                                best_move = (k, idx1, idx2)
                        else:
                            # Not tabu, evaluate it as a candidate move
                            if new_cost < current_best_cost:  # Could be improving or non-improving
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost
                                best_move = (k, idx1, idx2)

            if k == 0:
                # Swap round (indices refer to rounds, not teams)
                for idx1 in range((num_teams - 1) * 2):
                    for idx2 in range(idx1 + 1, (num_teams - 1) * 2):
                        # Swap round
                        new_schedule = swap_round(copy.deepcopy(current_schedule), idx1, idx2)

                        # Check if the resulting schedule is feasible
                        if count_violations(new_schedule) > 0:
                            continue  # Skip if the new schedule has violations

                        new_cost = heuristic_func(new_schedule)

                        # Aspiration criterion: Accept tabu move if it improves global best
                        if (k, idx1, idx2) in tabu_list:
                            if new_cost < best_cost:  # Aspiration criterion
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost
                                best_move = (k, idx1, idx2)
                        else:
                            # Not tabu, evaluate it as a candidate move
                            if new_cost < current_best_cost:  # Could be improving or non-improving
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost
                                best_move = (k, idx1, idx2)


        # If we found a valid (feasible) move, apply it
        if current_best_schedule is not None:
            current_schedule = current_best_schedule  # Update the current solution
            idle_iterations = 0  # Reset idle iterations if an improvement is found

            # Update the global best if needed
            if current_best_cost < best_cost:
                best_schedule = current_best_schedule
                best_cost = current_best_cost
                print(f"New best cost: {best_cost}")
                idle_rounds = 0  # Reset idle rounds since global improvement is found
            else:
                idle_rounds += 1  # Increment idle rounds if no global improvement is found

            # Add the move to the tabu list and manage the size of the tabu list
            if best_move:
                tabu_list[best_move] = iteration + num_teams
                tabu_order.append(best_move)

                # If the tabu list exceeds the maximum size, remove the oldest entry
                if len(tabu_list) > num_teams:
                    oldest_move = tabu_order.pop(0)  # Get the oldest move
                    tabu_list.pop(oldest_move, None)  # Remove it from the tabu list

                print(best_move)
                print(current_best_cost)
                print(tabu_list)
                # input()

        else:
            idle_iterations += 1  # No improvement found in this iteration, increment idle iterations
        
        iteration += 1  # Increment the iteration counter

    return best_schedule, best_cost


# def tabu_search(schedule, distance_matrix, heuristic_func, t_min=5, t_max=10, max_idle_iterations=10):
#     num_teams = len(schedule)
    
#     # Initialize the tabu list and related parameters
#     tabu_list = {}  # Dictionary to store tabu moves with their iteration expiration
#     iteration = 0   # Keep track of the iteration number
#     best_schedule = copy.deepcopy(schedule)  # Global best solution
#     current_schedule = copy.deepcopy(schedule)  # The current solution being explored
#     best_cost = heuristic_func(best_schedule)
    
#     idle_iterations = 0  # Counter for idle iterations
    
#     while idle_iterations < max_idle_iterations:
#         # print(tabu_list)
#         current_best_schedule = None
#         current_best_cost = float('inf')
#         best_move = None  # Will hold the best move (k, idx1, idx2)
        
#         # Loop through the selected neighborhood operations (k = 0, 1, 2)
#         for k in range(3):  # Only considering k = 0, k = 1, k = 2

#             if k == 1 or k == 2:
#                 # Swap home or swap team (2 indices needed)
#                 for idx1 in range(num_teams):
#                     for idx2 in range(idx1 + 1, num_teams):
                        
#                         if k == 1:
#                             # Swap home
#                             new_schedule = swap_home(copy.deepcopy(current_schedule), idx1, idx2)
#                         if k == 2:
#                             # Swap team
#                             new_schedule = swap_team(copy.deepcopy(current_schedule), idx1, idx2)

#                         # Check if the resulting schedule is feasible
#                         if count_violations(new_schedule) > 0:
#                             continue  # Skip if the new schedule has violations

#                         new_cost = heuristic_func(new_schedule)

#                         # Aspiration criterion: Accept tabu move if it improves global best
#                         if (k, idx1, idx2) in tabu_list and tabu_list[(k, idx1, idx2)] >= iteration:
#                             if new_cost < best_cost:  # Aspiration criterion
#                                 current_best_schedule = new_schedule
#                                 current_best_cost = new_cost
#                                 best_move = (k, idx1, idx2)
#                         else:
#                             # Not tabu, evaluate it as a candidate move
#                             if new_cost < current_best_cost:  # Could be improving or non-improving
#                                 current_best_schedule = new_schedule
#                                 current_best_cost = new_cost
#                                 best_move = (k, idx1, idx2)

#             if k == 0:
#                 # Swap round (indices refer to rounds, not teams)
#                 for idx1 in range((num_teams - 1) * 2):
#                     for idx2 in range(idx1 + 1, (num_teams - 1) * 2):
#                         # Swap round
#                         new_schedule = swap_round(copy.deepcopy(current_schedule), idx1, idx2)

#                         # Check if the resulting schedule is feasible
#                         if count_violations(new_schedule) > 0:
#                             continue  # Skip if the new schedule has violations

#                         new_cost = heuristic_func(new_schedule)

#                         # Aspiration criterion: Accept tabu move if it improves global best
#                         if (k, idx1, idx2) in tabu_list and tabu_list[(k, idx1, idx2)] >= iteration:
#                             if new_cost < best_cost:  # Aspiration criterion
#                                 current_best_schedule = new_schedule
#                                 current_best_cost = new_cost
#                                 best_move = (k, idx1, idx2)
#                         else:
#                             # Not tabu, evaluate it as a candidate move
#                             if new_cost < current_best_cost:  # Could be improving or non-improving
#                                 current_best_schedule = new_schedule
#                                 current_best_cost = new_cost
#                                 best_move = (k, idx1, idx2)

        
#         # If we found a valid (feasible) move, apply it
#         if current_best_schedule is not None:
#             current_schedule = current_best_schedule  # Update the current solution
#             if current_best_cost < best_cost:  # Update global best if needed
#                 best_schedule = current_best_schedule
#                 best_cost = current_best_cost
#                 # print("global best", best_cost)
#             idle_iterations = 0  # Reset idle counter

#             # Add the move to the tabu list
#             if best_move:
#                 tabu_list[best_move] = iteration + random.randint(t_min, t_max)
            
#             print(best_move)
#             print(current_best_cost)
#             print(tabu_list)
#             input()

#         else:
#             idle_iterations += 1  # No improvement found in this iteration
#             print(idle_iterations)
        
#         iteration += 1  # Increment the iteration counter

#     return best_schedule, best_cost



# Example call (this would be part of your main routine):

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]  # sys.argv[1] is the first command-line argument

else:
    print("No arguments provided.")
    sys.exit(1)


file_path = './Instances/{}.xml'.format(filename)
distance_matrix = read_xml_and_create_distance_matrix(file_path)

start_time = time.time()


num_teams = len(distance_matrix)

schedule_str = '''
Team  1's Schedule: [ -5  -3   6   2  -6  -4  -2   4   3   5]
Team  2's Schedule: [  3   4  -5  -1   5   6   1  -6  -4  -3]
Team  3's Schedule: [ -2   1   4  -6  -4   5   6  -5  -1   2]
Team  4's Schedule: [ -6  -2  -3   5   3   1  -5  -1   2   6]
Team  5's Schedule: [  1   6   2  -4  -2  -3   4   3  -6  -1]
Team  6's Schedule: [  4  -5  -1   3   1  -2  -3   2   5  -4]'''

# initial_schedule = parse_schedule_to_array(schedule_str)
initial_schedule = generate_team_centric_schedule(num_teams)
initial_distance = calculate_total_distance(initial_schedule, distance_matrix)

print("initial schedule is")
output_schedule(initial_schedule)


optimal_schedule_str = '''
Team  1's Schedule: [  5   2   6  -3  -4  -6   3   4  -2  -5]
Team  2's Schedule: [ -6  -1  -5   4   5  -3  -4   6   1   3]
Team  3's Schedule: [ -4   5   4   1  -6   2  -1  -5   6  -2]
Team  4's Schedule: [  3  -6  -3  -2   1   5   2  -1  -5   6]
Team  5's Schedule: [ -1  -3   2   6  -2  -4  -6   3   4   1]
Team  6's Schedule: [  2   4  -1  -5   3   1   5  -2  -3  -4]'''

optimal_schedule = parse_schedule_to_array(optimal_schedule_str)




def distance_heuristic(schedule):
    return calculate_total_distance(schedule, distance_matrix)


def hamming_heuristic(schedule):
    """
    Calculate the Hamming distance between two 2D lists of schedules.
    This function compares corresponding elements from two schedules and counts the number of differences.
    
    Parameters:
    schedule1, schedule2: List[List[int]]
        Two schedules to compare, where each schedule is a list of team schedules.
        
    Returns:
    int: The total Hamming distance between the two schedules.
    """
    # Initialize the distance
    hamming_distance = 0
    
    # Iterate over teams and rounds
    for team_schedule1, team_schedule2 in zip(optimal_schedule, schedule):
        for round1, round2 in zip(team_schedule1, team_schedule2):
            if round1 != round2:
                hamming_distance += 1
                
    return hamming_distance

heuristic_func = distance_heuristic
# heuristic_func = hamming_heuristic

print(heuristic_func(initial_schedule))

improved_schedule, improved_cost = tabu_search(initial_schedule, heuristic_func)
output_schedule(improved_schedule)
print(calculate_total_distance(improved_schedule, distance_matrix))