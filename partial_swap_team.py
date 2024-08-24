# from common import output_schedule

def partial_swap_team(schedule, team1_idx, team2_idx, i):
    "partial swapping team!"
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

        ## return the opponent that might causes duplicates, with its venue, not in idx
        return opponent1_sign * (opponent1_idx + 1)
    

    # Track the current potential duplicate opponent in each team's schedule
    opponent1 = swap_in_one_round(i) ## the initial swap expected by this neighbourhood, triggers the following adjustments
    
    # Track the rounds whose opponents have been set for team1 and team2 which potentially cause duplicates
    duplicate_round_team1 = i
    
    # Iteratively swap until no duplicates remain in each team's schedule,
    # equivalent to the opponent to remove of one team exactly matches the opponent the other team wants and vice versa
    

    while True:
       
        # Find duplicate opponents in team1's schedule
        finish = 1
        for r in range(len(schedule[team1_idx])):
            if r != duplicate_round_team1 and schedule[team1_idx][r] == opponent1:
                duplicate_round_team1 = r
                # still conflicts
                finish = 0
                break

        if finish:
            break
        

        opponent1 = swap_in_one_round(duplicate_round_team1)
    
    return schedule

# def partial_swap_round(schedule, team1_idx, team2_idx):
#     """
#     This function swaps all matches in round1 and round2 except teams 
#     who have the same opponent in both rounds
#     """
#     # print("p s round")
#     num_teams = len(schedule)
#     # teamA_schedule = schedule[teamA_idx]
    
#     unaffected_teams = []
#     for team_idx in range(num_teams):
#         if abs(schedule[team_idx][round1_idx]) == abs(schedule[team_idx][round2_idx]):
#             unaffected_teams.append(team_idx)

#     for team_idx in range(num_teams):
#         if team_idx not in unaffected_teams:
#             schedule[team_idx][round1_idx], schedule[team_idx][round2_idx] = \
#             schedule[team_idx][round2_idx], schedule[team_idx][round1_idx]

#     return schedule


# # Example usage
# schedule = [
#     [6, -2, 4, 3, -5, -4, -3, 5, 2, -6],  # Team 1
#     [5, 1, -3, -6, 4, 3, 6, -4, -1, -5],  # Team 2
#     [-4, 5, 2, -1, 6, -2, 1, -6, -5, 4],  # Team 3
#     [3, 6, -1, -5, -2, 1, 5, 2, -6, -3],  # Team 4
#     [-2, -3, 6, 4, 1, -6, -4, -1, 3, 2],  # Team 5
#     [-1, -4, -5, 2, -3, 5, -2, 3, 4, 1],  # Team 6
# ]

# team1_idx = 1  # Team 1
# team2_idx = 3  # Team 2
# round_i = 8  # Day 1 (index 0)

# new_schedule = partial_swap_team(schedule, team1_idx, team2_idx, round_i)
# output_schedule(new_schedule)
