import json

# with open('schedule.json', 'r') as file:
#     schedule = json.load(file)

# find_pattern_in_schedule(schedule)

from common import output_schedule

## Buggy
def partial_swap_round(schedule, teamA_idx, round1_idx, round2_idx):
    """
    This function swaps A-B, C-D to A-C, B-D in round1, and vice versa in round 2
    """
    num_teams = len(schedule)
    teamA_schedule = schedule[teamA_idx]
    
    ## record this to decide A's sign in the schedule of C in round 1
    opponentC_sign_for_A = 1 if teamA_schedule[round2_idx] > 0 else -1

    teamB_idx = abs(teamA_schedule[round1_idx]) - 1
    teamC_idx = abs(teamA_schedule[round2_idx]) - 1

    # Swap the selected rounds for team_A, preserve the original number, say -4 1 to 1 -4
    teamA_schedule[round1_idx], teamA_schedule[round2_idx] = teamA_schedule[round2_idx], teamA_schedule[round1_idx]

    # output_schedule(schedule)
    
    ## TeamD is the team originally playing against C in round 1
    teamD_idx = -1
    for i in range(num_teams):
        # input()
        # print(abs(schedule[i][round1_idx]))
        if (abs(schedule[i][round1_idx]) == teamC_idx + 1) and (i != teamA_idx):
            teamD_idx = i
            break

    teamB_schedule = schedule[teamB_idx]
    teamD_schedule = schedule[teamD_idx]
    

    ## simply swap the 2 numbers in B and D's schedule just like in A
    teamB_schedule[round1_idx], teamB_schedule[round2_idx] = teamB_schedule[round2_idx], teamB_schedule[round1_idx]
    teamD_schedule[round1_idx], teamD_schedule[round2_idx] = teamD_schedule[round2_idx], teamD_schedule[round1_idx]

    ## record this to decide D's sign in the schedule of C in round 2
    opponentC_sign_for_D = 1 if teamD_schedule[round2_idx] > 0 else -1

    schedule[teamC_idx][round1_idx] = -opponentC_sign_for_A * (teamA_idx + 1)
    schedule[teamC_idx][round2_idx] = -opponentC_sign_for_D * (teamD_idx + 1)

    return schedule


# # Example usage
schedule = [
    [6, -2, 2, 3, -5, -4, -3, 5, 4, -6],  # Team 1
    [5, 1, -1, -5, 4, 3, 6, -4, -6, -3],  # Team 2
    [-4, 5, 4, -1, 6, -2, 1, -6, -5, 2],  # Team 3
    [3, 6, -3, -6, -2, 1, 5, 2, -1, -5],  # Team 4
    [-2, -3, 6, 2, 1, -6, -4, -1, 3, 4],  # Team 5
    [-1, -4, -5, 4, -3, 5, -2, 3, 2, 1],  # Team 6
    # [4, -3, 2, -4, 3, -2],  # Team 1
    # [3, -4, -1, -3, 4, 1],  # Team 2
    # [-2, 1, 4, 2, -1, -4],  # Team 3
    # [-1, 2, -3, 1, -2, 3]   # Team 4
]


    # [4, -3, 2, -4, 3, -2],  # Team 1
    # [3, 1, -1, -3, 4, -4],  # Team 2
    # [-2, 1, 4, 2, -1, -4],  # Team 3
    # [-1, 2, -3, 1, -2, 3]   # Team 4

team_idx = 1  # Team 1
r1 = 1  # Day 1
r2 = 8  # Day 2 (index 0)

new_schedule = partial_swap_round(schedule, team_idx, r1, r2)
new_schedule = output_schedule(schedule)