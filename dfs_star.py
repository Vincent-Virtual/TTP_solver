import math
import sys
from common import *
from neighbourhood import *

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

start_time = time.time()

# Initialize scheduling parameters
schedule = [[None for _ in range(n)] for _ in range(n)]
UB = float('inf')  # Initial upper bound set to infinity

# Placeholder for start time
start_time = time.time()

# Functions for lower bound, constraint propagation, and solution update
def lower_bound(schedule):
    """Calculate an optimistic lower bound for the partially constructed schedule."""
    # Placeholder lower bound calculation; replace with specific logic
    return 100

def propagate_constraints():
    """Constraint propagation function."""
    # Placeholder function that checks current schedule constraints
    return True

def update_best_solution():
    """Update the best solution if current solution improves UB."""
    global UB
    # Placeholder: Update UB with current schedule cost
    pass

# Functions for choosing teams
def choose_team1(round_number):
    """Choose team1 for the round based on some strategy."""
    # Placeholder: implement strategy to choose team1
    return 0

def choose_team2(team1, disallowed_teams, round_number):
    """Choose team2 to pair with team1, avoiding disallowed teams."""
    for team in range(n):
        if team != team1 and team not in disallowed_teams:
            return team
    return None  # No feasible opponent found

def undo_pairing(team1i, team2i, round_number):
    """Undo the last pairing in the schedule for specified teams and round."""
    schedule[team1i][round_number] = None
    schedule[team2i][round_number] = None


def undo_pairing(team1i, team2i, round_number):
    """Undo the last pairing in the schedule and record it to avoid cycles."""
    schedule[team1i][round_number] = None
    schedule[team2i][round_number] = None
    # Add to disallowed pairs to prevent revisiting this pairing in the same round
    disallowed_pairs.add((team1i, team2i, round_number))


disallowed_pairs = set()  # Initialize an empty set to store disallowed pairs

# Main DFS* loop with backtracking and cycle avoidance
i = 1
while i > 0:
    # Determine round from the current index
    r = math.ceil(2 * i / n)
    
    # Select the first team (team1) based on the current round
    team1i = choose_team1(r)
    
    # Choose a second team (team2) for pairing with team1
    team2i = None
    for team in range(n):
        if team != team1i and (team1i, team, r) not in disallowed_pairs:
            team2i = team
            break  # Stop at the first feasible team
    
    # If a feasible pairing is found, add it to the schedule
    if team2i is not None:
        schedule[team1i][r] = team2i  # Mark team1 playing at home
        schedule[team2i][r] = team1i  # Mark team2 playing away

    # Check bounds and constraints before moving to the next pairing
    if lower_bound(schedule) < UB and propagate_constraints():
        i += 1
        # If a complete schedule is reached, check if it’s the best solution
        if i == n * (n - 1):
            update_best_solution()  # Update UB if this is the best solution
            i -= 1
            undo_pairing(team1i, team2i, r)
    else:
        # Undo pairing and mark it as disallowed to avoid cycles
        undo_pairing(team1i, team2i, r)
        
        # If no feasible team2 is available, backtrack to the previous pairing
        if team2i is None:
            i -= 1
            if i > 0:
                # Undo pairing for previous index
                prev_r = math.ceil(2 * (i - 1) / n)
                prev_team1 = choose_team1(prev_r)
                prev_team2 = schedule[prev_team1][prev_r]
                undo_pairing(prev_team1, prev_team2, prev_r)

# Final output after DFS* search completes
print("Best solution found:", UB)
print("Time taken:", time.time() - start_time)