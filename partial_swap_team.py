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
        # Find duplicate opponents in team1's and team2's schedules
        
        finish = 1
        for r in range(len(schedule[team1_idx])):
            if r != duplicate_round_team1 and schedule[team1_idx][r] == opponent1_sign * (opponent1_idx + 1):
                duplicate_round_team1 = r
                finish = 0
                break
            # if r != r and abs(schedule[team2_idx][r1]) == opponent2_idx + 1:
            #     duplicate_round_team2 = r
        if finish:
            break
        

        opponent1_sign, opponent1_idx = swap_in_one_round(duplicate_round_team1)
        input()
        output_schedule(schedule)
    
    return schedule

# Example usage
schedule = [
    [5, 1, -3, -6, 4, 3, 6, -4, -1, -5],  # Team 1
    [3, 6, -1, -5, -2, 1, 5, 2, -6, -3]  # Team 2
]

team1_idx = 0  # Team 1
team2_idx = 1  # Team 2
round_i = 8  # Day 1 (index 0)

new_schedule = partial_swap_team(schedule, team1_idx, team2_idx, round_i)
# for idx, team_schedule in enumerate(new_schedule):
#     print(f"Team {idx + 1}'s Schedule: {team_schedule}")
