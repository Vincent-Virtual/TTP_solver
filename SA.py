import sys, random, math

from common import *
from ini_sche import generate_team_centric_schedule

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]  # sys.argv[1] is the first command-line argument

else:
    print("No arguments provided.")
    sys.exit(1)


file_path = './Instances/{}.xml'.format(filename)

distance_matrix = read_xml_and_create_distance_matrix(file_path)

# Initialize random schedule S and set best cost so far
num_teams = len(distance_matrix)

T0 = 1000        # Initial temperature
beta = 0.95      # Cooling factor
maxC = 8       # Number of iterations at each temperature
maxP = 100      # Maximum number of phases (temperature levels)

phase = 0

S = generate_team_centric_schedule(num_teams)
# S_prime = None
# S = find_random_schedule()
bestSoFar = calculate_total_distance(S, distance_matrix)
counter = 0

neighbourhoods = [swap_round, swap_home, swap_team, partial_swap_round, partial_swap_team]

# Start the main loop with a phase limit
while phase <= maxP:
    print("phase is ", phase)
    phase = 0
    counter = 0

    # Inner loop with a counter limit
    T = 1
    while counter <= maxC:
        print("counter is ", counter)
        # Select a random move from the neighborhood of S
        k = random.randint(0, 4)

        if k <= 2: ## first 3 simple swap methods
            idx1, idx2 = random.sample(range(num_teams), 2)
            S_prime = neighbourhoods[k](S, idx1, idx2)

        if k == 3:
            teamA_idx = random.randrange(num_teams)
            round1_idx, round2_idx = random.sample(range(num_teams), 2)
            S_prime = partial_swap_round(S, teamA_idx, round1_idx, round2_idx)

        if k == 4:
            i = random.randrange(num_teams) # a random round
            team1_idx, team2_idx = random.sample(range(num_teams), 2)
            S_prime = partial_swap_team(S, i, team1_idx, team2_idx)
        # m = select_random_move_from_neighborhood(S)
        # S_prime = apply_move(S, m)
        # print(k)
        # print(S_prime)
        # input()
        # print(cost_with_violations(S_prime, distance_matrix))
        # output_schedule(S_prime)

        # print(bestSoFar)

        # Check if the new schedule has a lower cost
        if cost_with_violations(S_prime, distance_matrix) < cost_with_violations(S, distance_matrix):
            accept = True
        else:
            # Accept with a probability based on simulated annealing
            delta = cost_with_violations(S_prime, distance_matrix) - cost_with_violations(S, distance_matrix)
            accept = True if random.random() < math.exp(-delta / T) else False

        # If accepted, update the current schedule
        if accept:
            S = S_prime
            # Update best cost so far if applicable
            if cost_with_violations(S_prime, distance_matrix) < bestSoFar:
                counter = 0
                phase = 0
                bestSoFar = cost_with_violations(S_prime, distance_matrix)
            else:
                counter += 1
        else:
            counter += 1
    
    # Increment phase and decrease temperature
    phase += 1
    T = T * beta

print(cost_with_violations(S, distance_matrix))
print(calculate_total_distance(S, distance_matrix))
output_schedule(S)