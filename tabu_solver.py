from ini_sche import generate_team_centric_schedule
from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *


import random
import copy
import time
import sys
from collections import deque

def tabu_search(schedule, heuristic_func, max_idle_iterations=300, max_idle_rounds=20):
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
    
    while idle_iterations < max_idle_iterations:
        print("idle iteration is ", idle_iterations)
        current_best_schedule = None
        current_best_cost = float('inf')
        best_move = None  # Will hold the best move (k, idx1, idx2, etc.)
        
        # Loop through the selected neighborhood operations (k = 0, 1, 2, 3, 4)
        for k in range(5):  # Considering k = 0, 1, 2, 3, 4
            if k == 1 or k == 2:
            # if k == 1:
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
                            # pass
                        else:
                            # Not tabu, evaluate it as a candidate move
                            if new_cost < current_best_cost:  # Could be improving or non-improving
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost
                                best_move = (k, idx1, idx2)

            # if k == 0:
            #     # Swap round (indices refer to rounds, not teams)
            #     for idx1 in range((num_teams - 1) * 2):
            #         for idx2 in range(idx1 + 1, (num_teams - 1) * 2):
            #             # Swap round
            #             new_schedule = swap_round(copy.deepcopy(current_schedule), idx1, idx2)

            #             # Check if the resulting schedule is feasible
            #             if count_violations(new_schedule) > 0:
            #                 continue  # Skip if the new schedule has violations

            #             new_cost = heuristic_func(new_schedule)

            #             # Aspiration criterion: Accept tabu move if it improves global best
            #             if (k, idx1, idx2) in tabu_list:
            #                 if new_cost < best_cost:  # Aspiration criterion
            #                     current_best_schedule = new_schedule
            #                     current_best_cost = new_cost
            #                     best_move = (k, idx1, idx2)
            #             else:
            #                 # Not tabu, evaluate it as a candidate move
            #                 if new_cost < current_best_cost:  # Could be improving or non-improving
            #                     current_best_schedule = new_schedule
            #                     current_best_cost = new_cost
            #                     best_move = (k, idx1, idx2)

            if k == 3:
                # Partial swap team (requires 3 indices: two teams and a round)
                for idx1 in range(num_teams):
                    for idx2 in range(idx1 + 1, num_teams):
                        for round_idx in range((num_teams - 1) * 2):
                            # Apply partial swap team
                            new_schedule, pivot_round_idx = partial_swap_team(copy.deepcopy(current_schedule), idx1, idx2, round_idx, True)
                            # output_schedule(new_schedule)
                            #2 teams facing each other
                            if pivot_round_idx == -1:
                                # print("pivot -1")
                                continue

                            # Check if the resulting schedule is feasible
                            if count_violations(new_schedule) > 0:
                                continue  # Skip if the new schedule has violations

                            new_cost = heuristic_func(new_schedule)

                            # print("after partial swap")
                            # Aspiration criterion: Accept tabu move if it improves global best
                            if (k, idx1, idx2, pivot_round_idx) in tabu_list:
                                # if new_cost < best_cost:  # Aspiration criterion
                                #     current_best_schedule = new_schedule
                                #     current_best_cost = new_cost
                                #     best_move = (k, idx1, idx2, pivot_round_idx)
                                pass
                            else:
                                # Not tabu, evaluate it as a candidate move
                                if new_cost < current_best_cost:  # Could be improving or non-improving
                                    current_best_schedule = new_schedule
                                    current_best_cost = new_cost
                                    best_move = (k, idx1, idx2, pivot_round_idx)
                            
    

            if k == 4:
                # Partial swap round (requires 3 indices: two rounds and a team)
                for round_idx1 in range((num_teams - 1) * 2):
                    for round_idx2 in range(round_idx1 + 1, (num_teams - 1) * 2):
                        for team_idx in range(num_teams):
                            
                            # Apply partial swap round
                            new_schedule, pivot_team_idx = partial_swap_round(copy.deepcopy(current_schedule), round_idx1, round_idx2, team_idx, True)
                            
                            if pivot_team_idx == -1: #facing the same opponent across rounds ???!!!
                                continue

                            # Check if the resulting schedule is feasible
                            if count_violations(new_schedule) > 0:
                                continue  # Skip if the new schedule has violations
                            
                            new_cost = heuristic_func(new_schedule)

                            # Aspiration criterion: Accept tabu move if it improves global best
                            if (k, round_idx1, round_idx2, pivot_team_idx) in tabu_list:
                                # if new_cost < best_cost:  # Aspiration criterion
                                #     current_best_schedule = new_schedule
                                #     current_best_cost = new_cost
                                #     best_move = (k, round_idx1, round_idx2, pivot_team_idx)
                                pass
                            else:
                                # Not tabu, evaluate it as a candidate move
                                if new_cost < current_best_cost:  # Could be improving or non-improving
                                    current_best_schedule = new_schedule
                                    current_best_cost = new_cost
                                    # print(new_cost)
                                    best_move = (k, round_idx1, round_idx2, pivot_team_idx)

        # print("in for loop")
        # If we found a valid (feasible) move, apply it
        if current_best_schedule is not None:
            # print("current not None")
            current_schedule = current_best_schedule  # Update the current solution

            # Update the global best if needed
            if current_best_cost < best_cost:
                best_schedule = current_best_schedule
                best_cost = current_best_cost
                print(f"New best cost: {best_cost}")
                idle_iterations = 0  # Reset idle iterations if an improvement is found
            else:
                idle_iterations += 1  # Increment idle rounds if no global improvement is found

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

        iteration += 1  # Increment the iteration counter

    return best_schedule, best_cost


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
Team  1's Schedule: [-12  -4   9  10  -6 -10  -8  12   7   3  -9  -2  -3   2   8  -7   5  11   4  -5   6 -11]
Team  2's Schedule: [ -4   7  -5  11 -10 -11  -6   4  -3   8   5   1  -8  -1   6   3 -12  -9  -7  12  10   9]
Team  3's Schedule: [ -8  -6   7  12  -9 -12 -11   8   2  -1  -7  -5   1   5  11  -2  10   4   6 -10   9  -4]
Team  4's Schedule: [  2   1  -8  -7 -12   7   5  -2 -11  -9   8  10   9 -10  -5  11   6  -3  -1  -6  12   3]
Team  5's Schedule: [-11   9   2   8  -7  -8  -4  11 -10 -12  -2   3  12  -3   4  10  -1  -6  -9   1   7   6]
Team  6's Schedule: [  7   3  12  -9   1   9   2  -7  -8  10 -12 -11 -10  11  -2   8  -4   5  -3   4  -1  -5]
Team  7's Schedule: [ -6  -2  -3   4   5  -4   9   6  -1  11   3  12 -11 -12  -9   1  -8 -10   2   8  -5  10]
Team  8's Schedule: [  3 -10   4  -5  11   5   1  -3   6  -2  -4   9   2  -9  -1  -6   7 -12  10  -7 -11  12]
Team  9's Schedule: [-10  -5  -1   6   3  -6  -7  10 -12   4   1  -8  -4   8   7  12 -11   2   5  11  -3  -2]
Team 10's Schedule: [  9   8 -11  -1   2   1  12  -9   5  -6  11  -4   6   4 -12  -5  -3   7  -8   3  -2  -7]
Team 11's Schedule: [  5  12  10  -2  -8   2   3  -5   4  -7 -10   6   7  -6  -3  -4   9  -1 -12  -9   8   1]
Team 12's Schedule: [  1 -11  -6  -3   4   3 -10  -1   9   5   6  -7  -5   7  10  -9   2   8  11  -2  -4  -8]'''

initial_schedule = parse_schedule_to_array(schedule_str)
# initial_schedule = generate_team_centric_schedule(num_teams)
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
            if round1 != abs(round2):
                hamming_distance += 1
                
    return hamming_distance

heuristic_func = distance_heuristic
# heuristic_func = hamming_heuristic

print(heuristic_func(initial_schedule))
# input()

improved_schedule, improved_cost = tabu_search(initial_schedule, heuristic_func)
output_schedule(improved_schedule)
print(improved_cost)
print(calculate_total_distance(improved_schedule, distance_matrix))