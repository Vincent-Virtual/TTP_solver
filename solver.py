from ini_sche import generate_team_centric_schedule
# from parse_solution import parse_schedule_to_array
from common import *
from neighbourhood import *

from SLS import *
from greedy import iterative_greedy_search

import random
import copy
import time
import sys
import json

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


# initial_schedule = parse_schedule_to_array(schedule_str)


initial_schedule = generate_team_centric_schedule(num_teams)


initial_distance = calculate_total_distance(initial_schedule, distance_matrix)

print("initial schedule is")
output_schedule(initial_schedule)

# print("initial violation is ", count_violations(initial_schedule))
# print("initial distance is ", initial_distance)
# print()


CSC_schedule = initial_schedule
CSC_distance = initial_distance
violations = count_violations(CSC_schedule)


if violations != 0:
    sys.exit(1)

print("distance is ", CSC_distance)


print()
# input()


max_iterations = 2000
improvements = 0

## aspiration
k = 0

S0_schedule = CSC_schedule


S0_distance = calculate_total_distance(S0_schedule, distance_matrix)



S_star = S0_schedule
best_distance = S0_distance

S_current = S0_schedule
S_distance = S0_distance


## main loop
for i in range(max_iterations):
    # print("k is ", k)

    S_prime = None

    # Locate one random schedule S_prime within the current neighbourhood
    # if can't find one within some checks, just use S_current
    j = 0
    while j < num_teams * 2:
        schedule1 = random_neighbour(copy.deepcopy(S_current), k)
        if count_violations(schedule1) == 0:
            S_prime = schedule1
            break
        j += 1
    
    # print("while loop end")
    ## if the previous loop can't find a feasible random neighbour
    if j == num_teams * 2:
        # print("can't find random neighbour")
        S_prime = S_current
    
    # if i >= 1950:
    #     S_2primes, new_distance = iterative_greedy_search(S_prime, neighbourhoods, distance_matrix, k)
    # else:
    S_2primes, new_distance = stochastic_local_search(S_prime, distance_matrix, k)

    # print(i, new_distance)

    if new_distance < S_distance:         ## f(S'') < f(S)
        S_current = S_2primes
        S_distance = new_distance

        S_star = S_current
        best_distance = S_distance

        # print("stay here")
        # print("k is ", k)
        print("improved", i, S_distance)
        improvements += 1

    else:
        k = (k+1)%3 ## change to 5 for partial swap team
        # if k == 1:
        #     k = 3
        # elif k == 3:
        #     k = 4
        # elif k == 4:
        #     k = 1
    
    # print(i, S_distance)
    # print("violation is", count_violations(S_current))
    # output_schedule(S_current)

end_time = time.time()


output_schedule(S_star)
# output_schedule_with_distances(S_star, distance_matrix)
# output_sign_schedule(S_star)
# print("output distance is ", best_distance)


# with open('schedule.json', 'w') as file:
#     file.write('[')  # Start of the array
#     for i, sublist in enumerate(S_star):
#         json_string = json.dumps(sublist)  # Convert sublist to JSON string
#         if i < len(S_star) - 1:
#             json_string += ','  # Add comma except for the last item
#         file.write(json_string + '\n')  # Write the json string and move to new line
#     file.write(']')  # End of the array

assert calculate_total_distance(S_star, distance_matrix) == best_distance, "they should be equal"

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
# print(f"Execution time: {elapsed_time} seconds")
print("improvement count is ", improvements)
print("result: {}, iterations: {}, time:{}".format(best_distance, max_iterations, elapsed_time))







