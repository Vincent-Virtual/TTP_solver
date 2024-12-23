from ini_sche import generate_team_centric_schedule
from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *


import random
import copy
import time
import sys



filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]  # sys.argv[1] is the first command-line argument

else:
    print("No arguments provided.")
    sys.exit(1)


file_path = './Instances/{}.xml'.format(filename)
distance_matrix = read_xml_and_create_distance_matrix(file_path)




num_teams = len(distance_matrix)

schedule_str = '''
Team  1's Schedule: [ -2  -6   4  10   6 -12 -10  -8  11   7  -5 -11   9  12  -9  -4  -3   8   3  -7   5   2]
Team  2's Schedule: [  1  11  -7  -9 -11   3   5  12  -3  -4   7   4   8 -10  -8  -5  10   6   9  -6 -12  -1]
Team  3's Schedule: [ -7  -8 -10   7   8  -2  12   5   2  -5  -9  -6   4  11  -4  10   1   9  -1 -12 -11   6]
Team  4's Schedule: [ 11  12  -1 -11 -12   5   6   7  -6   2  10  -2  -3   8   3   1  -5  -7 -10   9  -8  -9]
Team  5's Schedule: [-12 -10  -9   6  10  -4  -2  -3   8   3   1  -7  11   9 -11   2   4  12  -6  -8  -1   7]
Team  6's Schedule: [  9   1  12  -5  -1   8  -4  11   4  -9 -11   3 -10  -7  10  -8 -12  -2   5   2   7  -3]
Team  7's Schedule: [  3   9   2  -3  -9 -10  11  -4  10  -1  -2   5  12   6 -12 -11  -8   4   8   1  -6  -5]
Team  8's Schedule: [-10   3  11  12  -3  -6  -9   1  -5 -11 -12   9  -2  -4   2   6   7  -1  -7   5   4  10]
Team  9's Schedule: [ -6  -7   5   2   7 -11   8 -10  12   6   3  -8  -1  -5   1 -12  11  -3  -2  -4  10   4]
Team 10's Schedule: [  8   5   3  -1  -5   7   1   9  -7 -12  -4  12   6   2  -6  -3  -2  11   4 -11  -9  -8]
Team 11's Schedule: [ -4  -2  -8   4   2   9  -7  -6  -1   8   6   1  -5  -3   5   7  -9 -10  12  10   3 -12]
Team 12's Schedule: [  5  -4  -6  -8   4   1  -3  -2  -9  10   8 -10  -7  -1   7   9   6  -5 -11   3   2  11]'''

# initial_schedule = parse_schedule_to_array(schedule_str)
initial_schedule = generate_team_centric_schedule(num_teams)
initial_distance = calculate_total_distance(initial_schedule, distance_matrix)

print("initial schedule is")
output_schedule(initial_schedule)


def distance_heuristic(schedule):
    return calculate_total_distance(schedule, distance_matrix)


optimal_schedule_str = '''
Team  1's Schedule: [  5   2   6  -3  -4  -6   3   4  -2  -5]
Team  2's Schedule: [ -6  -1  -5   4   5  -3  -4   6   1   3]
Team  3's Schedule: [ -4   5   4   1  -6   2  -1  -5   6  -2]
Team  4's Schedule: [  3  -6  -3  -2   1   5   2  -1  -5   6]
Team  5's Schedule: [ -1  -3   2   6  -2  -4  -6   3   4   1]
Team  6's Schedule: [  2   4  -1  -5   3   1   5  -2  -3  -4]'''
optimal_schedule = parse_schedule_to_array(optimal_schedule_str)

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

num_teams = len(initial_schedule)
tabu_list = {}
iteration = 0
best_schedule = copy.deepcopy(initial_schedule)
current_schedule = copy.deepcopy(initial_schedule)
best_cost = heuristic_func(best_schedule)


def find_best_move(k, current_schedule, heuristic_func):
    num_teams = len(current_schedule)
    
    ## to track the best move in the current neighbourhood, not globally
    current_best_schedule = None
    current_best_cost = float('inf')
    best_move = None

    if k == 1:  # Swap home
        for idx1 in range(num_teams):
            for idx2 in range(idx1 + 1, num_teams):
                new_schedule = swap_home(copy.deepcopy(current_schedule), idx1, idx2)
                if count_violations(new_schedule) > 0:
                    continue  # Skip if the new schedule has violations
                new_cost = heuristic_func(new_schedule)
                if (k, idx1, idx2) not in tabu_list or new_cost < best_cost:  # Aspiration criterion
                    if new_cost < current_best_cost:
                        current_best_schedule = new_schedule
                        current_best_cost = new_cost
                        best_move = (k, idx1, idx2)

    elif k == 2:  # Swap team
        for idx1 in range(num_teams):
            for idx2 in range(idx1 + 1, num_teams):
                new_schedule = swap_team(copy.deepcopy(current_schedule), idx1, idx2)
                if count_violations(new_schedule) > 0:
                    continue  # Skip if the new schedule has violations
                new_cost = heuristic_func(new_schedule)
                if (k, idx1, idx2) not in tabu_list or new_cost < best_cost: # Aspiration criterion
                    if new_cost < current_best_cost:
                        current_best_schedule = new_schedule
                        current_best_cost = new_cost
                        best_move = (k, idx1, idx2)

    elif k == 0:  # Swap round
        for idx1 in range((num_teams - 1) * 2):
            for idx2 in range(idx1 + 1, (num_teams - 1) * 2):
                new_schedule = swap_round(copy.deepcopy(current_schedule), idx1, idx2)
                if count_violations(new_schedule) > 0:
                    continue  # Skip if the new schedule has violations
                new_cost = heuristic_func(new_schedule)
                if (k, idx1, idx2) not in tabu_list or new_cost < best_cost: # Aspiration criterion
                    if new_cost < current_best_cost:
                        current_best_schedule = new_schedule
                        current_best_cost = new_cost
                        best_move = (k, idx1, idx2)

    elif k == 3:  # Partial swap team
        for idx1 in range(num_teams):
            for idx2 in range(idx1 + 1, num_teams):
                for round_idx in range((num_teams - 1) * 2):
                    new_schedule, pivot_round_idx = partial_swap_team(copy.deepcopy(current_schedule), idx1, idx2, round_idx, True)
                    if pivot_round_idx == -1:
                        continue
                    if count_violations(new_schedule) > 0:
                        continue  # Skip if the new schedule has violations
                    new_cost = heuristic_func(new_schedule)
                    if (k, idx1, idx2, pivot_round_idx) not in tabu_list or new_cost < best_cost: ## Aspiration criterion
                        if new_cost < current_best_cost:
                            current_best_schedule = new_schedule
                            current_best_cost = new_cost
                            best_move = (k, idx1, idx2, pivot_round_idx)

    elif k == 4:  # Partial swap round
        for round_idx1 in range((num_teams - 1) * 2):
            for round_idx2 in range(round_idx1 + 1, (num_teams - 1) * 2):
                for team_idx in range(num_teams):
                    new_schedule, pivot_team_idx = partial_swap_round(copy.deepcopy(current_schedule), round_idx1, round_idx2, team_idx, True)
                    if pivot_team_idx == -1:
                        continue
                    if count_violations(new_schedule) > 0:
                        continue  # Skip if the new schedule has violations
                    new_cost = heuristic_func(new_schedule)
                    if (k, round_idx1, round_idx2, pivot_team_idx) not in tabu_list or new_cost < best_cost: # Aspiration criterion
                        if new_cost < current_best_cost:
                            current_best_schedule = new_schedule
                            current_best_cost = new_cost
                            best_move = (k, round_idx1, round_idx2, pivot_team_idx)

    return current_best_schedule, current_best_cost, best_move


start_time = time.time()

max_idle_iterations = 200
improvements = 0
idle_iterations = 0

while idle_iterations < max_idle_iterations:
    moves_to_remove = []

    # print(tabu_list)
    # Iterate over all moves in the tabu_list
    for move in list(tabu_list.keys()):
        # Check if the tabu tenure of the move has expired
        if tabu_list[move] == iteration:
            # print("expired!")
            # If expired, mark it for removal
            moves_to_remove.append(move)

    # Remove expired moves from the tabu_list and tabu_order
    for move in moves_to_remove:
        tabu_list.pop(move)

    # print(tabu_list)
    # input()

    current_best_schedule = None
    current_best_cost = float('inf')
    best_move = None

    # Explore each neighborhood (k = 0, 1, 2, 3, 4)
    for k in range(5):
        new_schedule, new_cost, move = find_best_move(k, current_schedule, heuristic_func)

        # If the new move is better, update the best for this iteration
        if new_schedule is not None and new_cost < current_best_cost:
            current_best_schedule = new_schedule
            current_best_cost = new_cost
            best_move = move

    #  print(best_move)

    # Apply the best found move
    if current_best_schedule is not None:
        current_schedule = current_best_schedule
        if current_best_cost < best_cost:
            best_schedule = current_best_schedule
            best_cost = current_best_cost
            print(f"New best cost: {best_cost}")
            if best_cost == 0:
                break
            improvements += 1
            idle_iterations = 0
        else:
            idle_iterations += 1

        # Add the best move to the tabu list and manage size
        tabu_list[best_move] = iteration + num_teams * 2

    iteration += 1
    # print(idle_iterations)
    # print("best cost in current iteration is", current_best_cost)
    # print(tabu_list)

end_time = time.time()

output_schedule(best_schedule)
print(calculate_total_distance(best_schedule, distance_matrix))

elapsed_time = end_time - start_time
print("time: ", elapsed_time)
print("improvement count is ", improvements)