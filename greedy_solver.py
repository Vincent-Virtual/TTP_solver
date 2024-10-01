from ini_sche import generate_team_centric_schedule
from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *


import random
import copy
import time
import sys

##buggy

def calculate_hamming_distance(schedule1, schedule2):
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
    for team_schedule1, team_schedule2 in zip(schedule1, schedule2):
        for round1, round2 in zip(team_schedule1, team_schedule2):
            if round1 != round2:
                hamming_distance += 1
                
    return hamming_distance

def greedy_search(schedule, distance_matrix):
    num_teams = len(schedule)
    
    # Initialize the best schedule and cost
    best_schedule = copy.deepcopy(schedule)
    best_cost = calculate_total_distance(best_schedule, distance_matrix)
    improved = True  # Flag to track if an improvement was found
    
    while improved:
        improved = False  # Assume no improvement initially
        current_best_schedule = copy.deepcopy(best_schedule)
        current_best_cost = best_cost
        
        # Loop through all possible neighborhood operations
        for k in range(5):  # k ranges from 0 to 4, representing the 5 neighborhood operations
            # new_schedule = None

            # Apply the appropriate neighborhood operation based on k
            if k == 1 or k == 2:
                # idx1 < idx2 to break symmetry
                for idx1 in range(num_teams):
                    for idx2 in range(idx1 + 1, num_teams):
                        
                        if k == 1:
                            # Swap home
                            new_schedule = swap_home(copy.deepcopy(best_schedule), idx1, idx2)
                        if k == 2:
                            # Swap team
                            new_schedule = swap_team(copy.deepcopy(best_schedule), idx1, idx2)

                        # Check if the new schedule is better
                        if count_violations(new_schedule) == 0:
                            new_cost = calculate_total_distance(new_schedule, distance_matrix)
                            if new_cost < current_best_cost:
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost

            if k == 4:
                # Partial swap team requires an additional index (other_idx)
                for idx1 in range(num_teams):
                    for idx2 in range(idx1 + 1, num_teams):
                        for other_idx in range((num_teams - 1) * 2):
                            new_schedule = partial_swap_team(copy.deepcopy(best_schedule), idx1, idx2, other_idx)
                            if count_violations(new_schedule) == 0:
                                new_cost = calculate_total_distance(new_schedule, distance_matrix)
                                if new_cost < current_best_cost:
                                    print("k=4 update")
                                    current_best_schedule = new_schedule
                                    current_best_cost = new_cost

            if k == 0:
                for idx1 in range((num_teams - 1) * 2):
                    for idx2 in range(idx1 + 1, (num_teams - 1) * 2):

                        # Swap round
                        new_schedule = swap_round(copy.deepcopy(best_schedule), idx1, idx2)

                        # Check if the new schedule is better
                        if count_violations(new_schedule) == 0:
                            new_cost = calculate_total_distance(new_schedule, distance_matrix)
                            if new_cost < current_best_cost:
                                current_best_schedule = new_schedule
                                current_best_cost = new_cost

            if k == 3:
                for idx1 in range((num_teams - 1) * 2):
                    for idx2 in range(idx1 + 1, (num_teams - 1) * 2):
                        # Partial swap round requires an additional index (other_idx)
                        for other_idx in range(num_teams):
                            new_schedule = partial_swap_round(copy.deepcopy(best_schedule), idx1, idx2, other_idx)
                            if count_violations(new_schedule) == 0:
                                # print("here?")
                                new_cost = calculate_total_distance(new_schedule, distance_matrix)
                                if new_cost < current_best_cost:
                                    print("k=3 update")
                                    current_best_schedule = new_schedule
                                    current_best_cost = new_cost
        
        # If we found an improvement, apply the best move
        if current_best_cost < best_cost:
            best_schedule = current_best_schedule
            best_cost = current_best_cost
            print(best_cost)
            improved = True  # We found an improvement, so continue the search

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

print("initial violation is ", count_violations(initial_schedule))
print("initial distance is ", initial_distance)
print()

# neighbourhoods = [swap_round, swap_home, swap_team, partial_swap_round, partial_swap_team]
# neighbourhoods = [swap_home, partial_swap_round, partial_swap_team]

improved_schedule, improved_cost = greedy_search(initial_schedule, distance_matrix)
output_schedule(improved_schedule)
print(calculate_total_distance(improved_schedule, distance_matrix))