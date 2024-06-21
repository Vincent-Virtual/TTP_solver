from ini_sche import generate_team_centric_schedule

from common import read_xml_and_create_distance_matrix, output_schedule, calculate_total_distance, \
swap_round, swap_home, swap_team, count_violations, cost_with_violations

from simulated_annealing import initial_sa
from SLS import local_search, stochastic_local_search

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

# print("Distance matrix:", distance_matrix)
num_teams = len(distance_matrix)

initial_schedule = generate_team_centric_schedule(num_teams)

#A "distance_matrix" argument means this is "general SA" method
initial_distance = calculate_total_distance(initial_schedule, distance_matrix)

print("initial schedule is")
output_schedule(initial_schedule)
# input()
print("initial violation is ", count_violations(initial_schedule))
# input()
print("initial distance is ", initial_distance)
print()

# S_current = current_schedule
# S_cost = current_cost

CSC_schedule = initial_sa(copy.deepcopy(initial_schedule), distance_matrix)
# S_current = initial_sa(copy.deepcopy(current_schedule))
CSC_distance = calculate_total_distance(CSC_schedule, distance_matrix)

print("after SA")
output_schedule(CSC_schedule)
print("violation is ", count_violations(CSC_schedule))
print("distance is ", CSC_distance)


print()
# input()


max_iterations = 2000
neighbourhoods = [swap_round, swap_home, swap_team]

## aspiration
k = 0
i0 = -1
j0 = -1

dist = 10000000000000000000000
for i in range(num_teams - 1):
    for j in range(i+1, num_teams):
        schedule1 = swap_round(copy.deepcopy(CSC_schedule), i, j)
        if count_violations(schedule1) == 0:
            dist1 = calculate_total_distance(schedule1, distance_matrix)
            if dist1 < dist:
                dist = dist1
                i0 = i
                j0 = j


S0_schedule = swap_round(CSC_schedule, i0, j0)
S0_distance = dist

S_star = S0_schedule
best_distance = S0_distance

S_current = S0_schedule
S_distance = S0_distance


## main loop
for i in range(max_iterations):

    S_prime = None

    while True:
        idx1, idx2 = random.sample(range(num_teams), 2)

            # Generate the neighbor by swapping home/away status between the two teams
        schedule1 = neighbourhoods[k](copy.deepcopy(S_current), idx1, idx2)  # Create a deep copy
        if count_violations(schedule1) == 0:
            S_prime = schedule1
            break

    S_2primes, new_distance = stochastic_local_search(S_prime, neighbourhoods[k], distance_matrix)

    if new_distance < S_distance:         ## f(S'') < f(S)
        S_current = S_2primes
        S_distance = new_distance

        S_star = S_current
        best_distance = S_distance

        print(i, S_distance)

    else:
        k = (k+1)%3
    
    # print(i, S_distance)

end_time = time.time()

output_schedule(S_star)
print("violation is ", count_violations(S_star))
print("output distance is ", best_distance)

with open('schedule.json', 'w') as file:
    json.dump(S_star, file)

assert calculate_total_distance(S_star, distance_matrix) == best_distance, "they should be equal"

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")







