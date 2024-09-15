import random
import math
import copy
from ini_sche import generate_team_centric_schedule
from common import *
from neighbourhood import *


# General SA
def initial_sa(initial_schedule, distance_matrix, initial_temp = 1000):
    num_rounds = len(initial_schedule)

    current_temp = initial_temp

    current_schedule = initial_schedule
    current_cost = cost_with_violations(initial_schedule, distance_matrix)


    max_iterations = 10000
    cooling_rate = 0.9

    for _ in range(max_iterations):
        round1_idx, round2_idx = random.sample(range(num_rounds), 2)
        new_schedule = swap_round(copy.deepcopy(current_schedule), round1_idx, round2_idx)
        new_cost = cost_with_violations(new_schedule, distance_matrix)
        cost_diff = new_cost - current_cost
        # print(new_cost)
        
        if cost_diff < 0 or random.random() < math.exp(-cost_diff / current_temp): ## accept this move
            current_schedule = new_schedule
            current_cost = new_cost
            
            # if new_cost < best_cost: ## check the accepted move is the current best
            #     best_schedule = new_schedule
            #     best_cost = new_cost
            #     print("best updated")
            current_temp *= cooling_rate
        
        # if current_temp < 1e-3:
        #     break

    return current_schedule

