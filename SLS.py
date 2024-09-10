import copy
import random
from common import cost_with_violations, count_violations, calculate_total_distance

def random_neighbour(schedule, neighbourhoods: list, k):
    num_teams = len(schedule)

    # idx1 < idx2 to break symmetry
    idx1, idx2 = sorted(random.sample(range(num_teams), 2))
    # idx1, idx2 = random.sample(range(num_teams), 2)

    if k <= 2:
        return neighbourhoods[k](schedule, idx1, idx2)
    
    if k == 3:
        other_idx = random.randrange(num_teams)
        return neighbourhoods[k](schedule, idx1, idx2, other_idx)
    
    if k == 4:
        other_idx = random.randrange((num_teams-1) * 2)
        return neighbourhoods[k](schedule, idx1, idx2, other_idx)

def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k, max_iterations=120):
    
    # Initialize the best schedule and cost
    best_schedule = copy.deepcopy(schedule)
    best_cost = calculate_total_distance(best_schedule, distance_matrix)
    
    for _ in range(max_iterations):
        # Generate a random neighbor from the current best schedule
        new_schedule = random_neighbour(copy.deepcopy(best_schedule), neighbourhoods, k)

        # Check if there are no violations
        if count_violations(new_schedule) == 0:
            new_cost = calculate_total_distance(new_schedule, distance_matrix)

            # If the new schedule improves the cost, update the best schedule and continue from there
            if new_cost < best_cost:
                best_schedule = new_schedule
                best_cost = new_cost
    
    return best_schedule, best_cost


# def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k):




#     n = len(schedule)
#     new_schedule = schedule
#     new_cost = calculate_total_distance(new_schedule, distance_matrix)
    
#     while True:

#         schedule1 = random_neighbour(copy.deepcopy(schedule), neighbourhoods, k)

#         if count_violations(schedule1) == 0:
#             new_schedule = schedule1
#             new_cost = calculate_total_distance(schedule1, distance_matrix)
#             break
        
#     return new_schedule, new_cost
