from common import output_schedule

def partial_swap_team(schedule, team1_idx, team2_idx, i):
    ## handles the swap of the 2 teams only within one round r
    def swap_in_one_round(r):
        # Find the opponents of team1 and team2 on day i after this swap
        opponent1_idx = abs(schedule[team2_idx][r]) - 1  # Get opponent index for team1
        opponent2_idx = abs(schedule[team1_idx][r]) - 1  # Get opponent index for team2
        
        # Preserve the home/away status for team1 and team2
        opponent1_sign = 1 if schedule[team1_idx][r] > 0 else -1
        opponent2_sign = 1 if schedule[team2_idx][r] > 0 else -1
        
        # print(team1_sign * opponent1_idx)
        # Swap the opponents but keep the home/away status the same
        schedule[team1_idx][r], schedule[team2_idx][r] = (opponent1_sign * (opponent1_idx+1), opponent2_sign * (opponent2_idx+1))

        # resolve mismatches in the round after swapping 2 teams
        affected_team1_idx = abs(schedule[team1_idx][r]) - 1
        affected_team2_idx = abs(schedule[team2_idx][r]) - 1
        # print(affected_team1, affected_team2)

        schedule[affected_team1_idx][r], schedule[affected_team2_idx][r] = \
        schedule[affected_team2_idx][r], schedule[affected_team1_idx][r]

        if schedule[team1_idx][r] > 0:
            schedule[affected_team1_idx][r] = -abs(schedule[affected_team1_idx][r])
        else:
            schedule[affected_team1_idx][r] = abs(schedule[affected_team1_idx][r])

        if schedule[team2_idx][r] > 0:
            schedule[affected_team2_idx][r] = -abs(schedule[affected_team2_idx][r])
        else:
            schedule[affected_team2_idx][r] = abs(schedule[affected_team2_idx][r])
        return opponent1_sign, opponent1_idx
    

    # Track the current potential duplicate opponent in each team's schedule
    opponent1_sign, opponent1_idx = swap_in_one_round(i) ## the initial swap expected by this neighbourhood, triggers the following adjustments
    
    # Track the rounds whose opponents have been set for team1 and team2 which potentially cause duplicates
    duplicate_round_team1 = i
    # duplicate_round_team2 = i

    # Iteratively swap until no duplicates remain in each team's schedule,
    # equivalent to the opponent to remove of one team exactly matches the opponent the other team wants and vice versa
    
    # visited_rounds = set()
    while True:
        # input()
        output_schedule(schedule)

        # Find duplicate opponents in team1's and team2's schedules
        
        finish = 1
        for r in range(len(schedule[team1_idx])):
            if r != duplicate_round_team1 and schedule[team1_idx][r] == opponent1_sign * (opponent1_idx + 1):
                duplicate_round_team1 = r
                # still conflicts
                finish = 0
                break
            # if r != r and abs(schedule[team2_idx][r1]) == opponent2_idx + 1:
            #     duplicate_round_team2 = r
        if finish:
            break
        

        opponent1_sign, opponent1_idx = swap_in_one_round(duplicate_round_team1)

        
        
    
    return schedule


# # Example usage
# schedule = [
#     [4, -3, 2, -4, 3, -2],  # Team 1
#     [3, -4, -1, -3, 4, 1],  # Team 2
#     [-2, 1, 4, 2, -1, -4],  # Team 3
#     [-1, 2, -3, 1, -2, 3]   # Team 4
# ]

# team1_idx = 1  # Team 1
# team2_idx = 2  # Team 2
# round_i = 5  # Day 1 (index 0)

# new_schedule = partial_swap_team(schedule, team1_idx, team2_idx, round_i)
# output_schedule(new_schedule)
