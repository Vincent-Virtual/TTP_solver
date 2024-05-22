import random
import math
import copy
from ini_sche import generate_team_centric_schedule
from common import swap_round, calculate_total_distance, count_violations, cost_with_violations, output_schedule

# SA for VNS
# def initial_sa(SC_schedule, initial_temp = 10000, max_iterations = 10000, cooling_rate = 0.9):
#     num_rounds = len(SC_schedule)

#     S0_schedule = SC_schedule
#     temp = initial_temp
#     S_current = S0_schedule

#     for _ in range(max_iterations):
#         if count_violations(S_current) != 0:
#         #     S′ ← choose random configuration ∈ N(S)
#             round1_idx, round2_idx = random.sample(range(num_rounds), 2)
#             S_prime = swap_round(copy.deepcopy(S_current), round1_idx, round2_idx)
#             r = random.random() # random number btw 0 and 1
#             diff = count_violations(S_prime) - count_violations(S_current)
#             if r < math.exp( -diff / temp):
#                 S_current = S_prime ##the new starting solution is modified)
#                 temp = temp * cooling_rate
#         else:
#             break
            
#     return S_current


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

