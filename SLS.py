import copy
import random
from common import cost_with_violations, count_violations, calculate_total_distance

# def local_search(schedule, neighbourhood, distance_matrix):
#     best_neighbour = schedule
#     best_cost = cost_with_violations(schedule, distance_matrix)

#     n = len(schedule)
#     for i in range(n):
#         for j in range(i + 1, n):
#             # Generate the neighbour by swapping home/away status between the two teams
#             new_schedule = neighbourhood(copy.deepcopy(schedule), i, j)  # Create a deep copy
#             new_cost = cost_with_violations(new_schedule, distance_matrix)

#             # Check if the new schedule is better
#             if new_cost < best_cost:
#                 best_cost = new_cost
#                 best_neighbour = new_schedule

#     return best_neighbour, best_cost

def stochastic_local_search(schedule, neighbourhood, distance_matrix, k):

    n = len(schedule)
    new_schedule = schedule
    new_cost = calculate_total_distance(new_schedule, distance_matrix)

    while True:
        schedule1 = None

        if k == 3 or k == 4:
            other_idx = -100
            if k == 3:
                other_idx = random.randrange(n)
            if k == 4:
                other_idx = random.randrange((n-1) * 2)

            # print(start_round, n)
            idx1, idx2 = random.sample(range(n), 2)
            schedule1 = neighbourhood(copy.deepcopy(schedule), idx1, idx2, other_idx)
            
        else: # k = 0, 1, 2
            i, j = random.sample(range(n), 2)
            # Generate the neighbor by swapping home/away status between the two teams
            schedule1 = neighbourhood(copy.deepcopy(schedule), i, j)  # Create a deep copy
  

        if count_violations(schedule1) == 0:
            new_schedule = schedule1
            new_cost = calculate_total_distance(schedule1, distance_matrix)
            break
        
    return new_schedule, new_cost
