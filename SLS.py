import copy
import random
from common import cost_with_violations, count_violations, calculate_total_distance

def random_neighbour(schedule, neighbourhoods: list, k):
    num_teams = len(schedule)

    if k == 1 or k == 2 or k == 4:
        # idx1 < idx2 to break symmetry
        idx1, idx2 = sorted(random.sample(range(num_teams), 2))

        if k != 4:
            return neighbourhoods[k](schedule, idx1, idx2)
        
        if k == 4:
            other_idx = random.randrange((num_teams-1) * 2)
            return neighbourhoods[k](schedule, idx1, idx2, other_idx)

    ## k == 0 or k == 3     idx1, idx2 can be all round indices
    idx1, idx2 = sorted(random.sample(range((num_teams - 1) * 2), 2))

    if k == 0:
        # print((idx1, idx2))
        return neighbourhoods[k](schedule, idx1, idx2)
    
    if k == 3:
        other_idx = random.randrange(num_teams)
        # print((idx1, idx2, other_idx))
        return neighbourhoods[k](schedule, idx1, idx2, other_idx)
    
def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k):
    
    stagnation_threshold = 2 * len(schedule)

    # Initialize the best schedule and cost
    best_schedule = copy.deepcopy(schedule)
    best_cost = calculate_total_distance(best_schedule, distance_matrix)
    stagnation_counter = 0  # Counter to track stagnation in improvements

    while True:
        # Generate a random neighbor from the current best schedule
        new_schedule = random_neighbour(copy.deepcopy(best_schedule), neighbourhoods, k)

        # Check if there are no violations
        if count_violations(new_schedule) == 0:
            new_cost = calculate_total_distance(new_schedule, distance_matrix)

            # If the new schedule improves the cost, update the best schedule and reset the stagnation counter
            if new_cost < best_cost:
                best_schedule = new_schedule
                best_cost = new_cost
                stagnation_counter = 0  # Reset counter since we found a better solution
            else:
                stagnation_counter += 1  # Increment counter when no improvement

        # Check for stagnation
        if stagnation_counter >= stagnation_threshold:
            # print("stagnation happens")
            break  # Terminate if no improvement for the threshold number of iterations

    return best_schedule, best_cost

# def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k, max_iterations=30):
    
#     # Initialize the best schedule and cost
#     best_schedule = copy.deepcopy(schedule)
#     best_cost = calculate_total_distance(best_schedule, distance_matrix)
    
#     for _ in range(max_iterations):
#         # Generate a random neighbor from the current best schedule
#         new_schedule = random_neighbour(copy.deepcopy(best_schedule), neighbourhoods, k)

#         # Check if there are no violations
#         if count_violations(new_schedule) == 0:
#             new_cost = calculate_total_distance(new_schedule, distance_matrix)

#             # If the new schedule improves the cost, update the best schedule and continue from there
#             if new_cost < best_cost:
#                 best_schedule = new_schedule
#                 best_cost = new_cost
    
#     return best_schedule, best_cost


###
# Try to make tenure a function of n
###

# def random_neighbour1(schedule, neighbourhoods: list, k, tabu, current_iteration):
#     num_teams = len(schedule)
    
#     while True:
#         # idx1 < idx2 to break symmetry
#         idx1, idx2 = sorted(random.sample(range(num_teams), 2))
        
#         # Check if the swap is tabu
#         if tabu[idx1][idx2] <= current_iteration:
#             break  # Valid swap, not tabu
        
#     if k <= 2:
#         return neighbourhoods[k](schedule, idx1, idx2), (idx1, idx2)
    
#     if k == 3:
#         other_idx = random.randrange(num_teams)
#         return neighbourhoods[k](schedule, idx1, idx2, other_idx), (idx1, idx2, other_idx)
    
#     if k == 4:
#         other_idx = random.randrange((num_teams-1) * 2)
#         return neighbourhoods[k](schedule, idx1, idx2, other_idx), (idx1, idx2, other_idx)


# def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k, tabu_tenure = 8, max_iterations=30):
#     # print("k is ", k)

#     # Initialize tabu list with zeros
#     num_teams = len(schedule)
#     # tabu_tenure = num_teams
#     tabu = [[0] * num_teams for _ in range(num_teams)]
    
#     # Initialize the best schedule and cost
#     best_schedule = copy.deepcopy(schedule)
#     best_cost = calculate_total_distance(best_schedule, distance_matrix)
#     current_iteration = 0
    
#     for _ in range(max_iterations):
#         # Generate a random neighbor and the corresponding operation
#         new_schedule, operation = random_neighbour1(copy.deepcopy(best_schedule), neighbourhoods, k, tabu, current_iteration)

#         # Check if there are no violations
#         if count_violations(new_schedule) == 0:
#             new_cost = calculate_total_distance(new_schedule, distance_matrix)

#             # If the new schedule improves the cost, update the best schedule and continue from there
#             if new_cost < best_cost:
#                 best_schedule = new_schedule
#                 best_cost = new_cost

#             # Update the tabu list for the swapped indices
#             if len(operation) == 2:  # For neighbourhoods with two indices
#                 idx1, idx2 = operation
#                 tabu[idx1][idx2] = current_iteration + tabu_tenure  # Set tabu tenure
#             elif len(operation) == 3:  # For neighbourhoods with three indices
#                 idx1, idx2, _ = operation
#                 tabu[idx1][idx2] = current_iteration + tabu_tenure  # Set tabu tenure
        
#         # Increment the iteration counter
#         current_iteration += 1
    
#     return best_schedule, best_cost



# # Revised random_neighbour function without `while True`, limited by max_attempts
# def random_neighbour1(schedule, neighbourhoods: list, k, tabu, current_iteration, max_attempts=10):
#     num_teams = len(schedule)

#     for _ in range(max_attempts):
#         if k == 1 or k == 2 or k == 4:
#             # idx1 < idx2 to break symmetry
#             idx1, idx2 = sorted(random.sample(range(num_teams), 2))
#             # Check if the swap (with k) is not tabu
#             if (idx1, idx2, k) not in tabu or tabu[(idx1, idx2, k)] <= current_iteration:
#                 if k != 4:
#                     return neighbourhoods[k](schedule, idx1, idx2), (idx1, idx2, k)
#                 else:
#                     other_idx = random.randrange((num_teams - 1) * 2)
#                     return neighbourhoods[k](schedule, idx1, idx2, other_idx), (idx1, idx2, other_idx, k)

#         # k == 0 or k == 3: idx1, idx2 can be round indices
#         idx1, idx2 = sorted(random.sample(range((num_teams - 1) * 2), 2))
#         # Check if the swap (with k) is not tabu
#         if (idx1, idx2, k) not in tabu or tabu[(idx1, idx2, k)] <= current_iteration:
#             if k == 0:
#                 return neighbourhoods[k](schedule, idx1, idx2), (idx1, idx2, k)
#             elif k == 3:
#                 other_idx = random.randrange(num_teams)
#                 return neighbourhoods[k](schedule, idx1, idx2, other_idx), (idx1, idx2, other_idx, k)

#     # If all attempts were tabu, return the current schedule unchanged
#     return schedule, None  # No operation performed

# # Stochastic local search with limited neighbor attempts and tabu mechanism
# def stochastic_local_search(schedule, neighbourhoods, distance_matrix, k, tabu_tenure=5, max_iterations=30, max_attempts=10):
#     # Initialize tabu dictionary for tracking moves
#     tabu = {}
    
#     # Initialize the best schedule and cost
#     best_schedule = copy.deepcopy(schedule)
#     best_cost = calculate_total_distance(best_schedule, distance_matrix)
#     current_iteration = 0
    
#     for _ in range(max_iterations):
#         # Generate a random neighbor and the corresponding operation
#         new_schedule, operation = random_neighbour1(copy.deepcopy(best_schedule), neighbourhoods, k, tabu, current_iteration, max_attempts)

#         # If no valid move is found (operation is None), continue with the current best schedule
#         if operation is None:
#             continue  # Keep current best_schedule for the next iteration

#         # Check if there are no violations
#         if count_violations(new_schedule) == 0:
#             new_cost = calculate_total_distance(new_schedule, distance_matrix)

#             # If the new schedule improves the cost, update the best schedule
#             if new_cost < best_cost:
#                 best_schedule = new_schedule
#                 best_cost = new_cost

#             # Update the tabu list for the operation, using (idx1, idx2, k) as the key
#             if len(operation) == 3:  # For neighbourhoods with two indices and k
#                 idx1, idx2, k = operation
#                 tabu[(idx1, idx2, k)] = current_iteration + tabu_tenure  # Set tabu tenure
#             elif len(operation) == 4:  # For neighbourhoods with three indices and k
#                 idx1, idx2, other_idx, k = operation
#                 tabu[(idx1, idx2, other_idx, k)] = current_iteration + tabu_tenure  # Set tabu tenure
        
#         # Increment the iteration counter
#         current_iteration += 1
    
#     return best_schedule, best_cost
