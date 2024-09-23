# from ini_sche import generate_team_centric_schedule
# from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *

import random
import copy
import time
import sys
import json


# filename = ""
# if len(sys.argv) > 1:
#     filename = sys.argv[1]  # sys.argv[1] is the first command-line argument

# else:
#     print("No arguments provided.")
#     sys.exit(1)


# file_path = './Instances/{}.xml'.format(filename)
# distance_matrix = read_xml_and_create_distance_matrix(file_path)

# start_time = time.time()


# num_teams = len(distance_matrix)


# # initial_schedule = parse_schedule_to_array(schedule_str)
# initial_schedule = generate_team_centric_schedule(num_teams)
# initial_distance = calculate_total_distance(initial_schedule, distance_matrix)

# print("initial schedule is")
# output_schedule(initial_schedule)

# print("initial violation is ", count_violations(initial_schedule))
# print("initial distance is ", initial_distance)
# print()




# print()
# # input()


# max_iterations = 2000
# neighbourhoods = [swap_round, swap_home, swap_team, partial_swap_round, partial_swap_team]

def greedy_search(schedule, neighbourhoods, distance_matrix, k):
    num_teams = len(schedule)
    best_schedule = copy.deepcopy(schedule)
    best_cost = calculate_total_distance(best_schedule, distance_matrix)

    # Initialize variables to store the best found move
    best_move = None

    # Depending on the neighborhood k, generate possible moves
    if k == 1 or k == 2 or k == 4:
        # Neighborhoods that involve two teams
        for idx1 in range(num_teams):
            for idx2 in range(idx1 + 1, num_teams):  # idx1 < idx2 to avoid duplicate moves
                if k != 4:
                    new_schedule = neighbourhoods[k](copy.deepcopy(schedule), idx1, idx2)
                else:
                    for other_idx in range((num_teams - 1) * 2):
                        new_schedule = neighbourhoods[k](copy.deepcopy(schedule), idx1, idx2, other_idx)

                # Check if the new schedule is valid (no violations)
                if count_violations(new_schedule) == 0:
                    new_cost = calculate_total_distance(new_schedule, distance_matrix)

                    # If the new schedule improves the cost, update the best move
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_schedule = new_schedule
                        best_move = (idx1, idx2) if k != 4 else (idx1, idx2, other_idx)

    elif k == 0 or k == 3:
        # Neighborhoods that involve two rounds or rounds and a team
        for idx1 in range((num_teams - 1) * 2):
            for idx2 in range(idx1 + 1, (num_teams - 1) * 2):  # idx1 < idx2 to avoid duplicate moves
                if k == 0:
                    new_schedule = neighbourhoods[k](copy.deepcopy(schedule), idx1, idx2)
                elif k == 3:
                    for other_idx in range(num_teams):
                        new_schedule = neighbourhoods[k](copy.deepcopy(schedule), idx1, idx2, other_idx)

                        # Check if the new schedule is valid (no violations)
                        if count_violations(new_schedule) == 0:
                            new_cost = calculate_total_distance(new_schedule, distance_matrix)

                            # If the new schedule improves the cost, update the best move
                            if new_cost < best_cost:
                                best_cost = new_cost
                                best_schedule = new_schedule
                                best_move = (idx1, idx2, other_idx)

    print(f"Best move: {best_move} with cost: {best_cost}")
    return best_schedule, best_cost


def iterative_greedy_search(schedule, neighbourhoods, distance_matrix, k, max_iterations=20):
    current_schedule = copy.deepcopy(schedule)
    current_cost = calculate_total_distance(current_schedule, distance_matrix)

    for iteration in range(max_iterations):
        # print(f"Iteration {iteration + 1}: Current Cost = {current_cost}")

        # Apply the greedy search to find the best move in the neighborhood
        new_schedule, new_cost = greedy_search(current_schedule, neighbourhoods, distance_matrix, k)

        # Check if an improvement was found
        if new_cost < current_cost:
            current_schedule = new_schedule
            current_cost = new_cost
        else:
            # Stop if no further improvements can be found
            # print("No further improvements found. Terminating early.")
            break

    # print(f"Final Cost after {iteration + 1} iterations: {current_cost}")
    return current_schedule, current_cost


# iterative_greedy_search(initial_schedule, neighbourhoods, distance_matrix, 4)