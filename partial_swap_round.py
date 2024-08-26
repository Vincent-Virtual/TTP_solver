def partial_swap_round(schedule, round1_idx, round2_idx, teamA_idx):
    """
    This function swaps all matches in round1 and round2 except teams 
    who have the same opponent in both rounds
    """
    ## same opponent in both rounds, not valid
    if schedule[teamA_idx][round1_idx] == -schedule[teamA_idx][round2_idx]:
        return schedule

    num_teams = len(schedule)

    opponent1 = schedule[teamA_idx][round1_idx]
    opponent2 = schedule[teamA_idx][round2_idx]

    opponent1_idx = abs(opponent1) - 1
    opponent2_idx = abs(opponent2) - 1

    ## store the teams affected in the partial swap loop, swap them later on
    to_swap_teams = set() 
    to_swap_teams.add(teamA_idx)
    to_swap_teams.add(opponent1_idx)
    to_swap_teams.add(opponent2_idx)

    checking_opponent = opponent2

    ## Check if finally the opponent to reset coincides with oppo1 who triggers everything
    while abs(checking_opponent) != abs(opponent1):

        for team_idx in range(num_teams):
            ## Check which team will be affected as it will 
            ## potentially face another team twice in round1 after the previous swap
            if abs(schedule[team_idx][round1_idx]) == abs(checking_opponent):
                ## update the new conflict oppo in round2
                checking_opponent = schedule[team_idx][round2_idx]
                checking_opponent_idx = abs(checking_opponent) - 1
                to_swap_teams.add(checking_opponent_idx)
                to_swap_teams.add(team_idx)
                # print(team_idx, checking_opponent_idx)
                # input()
                # print(r, checking_opponent)
                break
    # print("ps round")
    ## The while loop will always break if DRR schedule as input
    ## perform the swaps here
    for team_idx in to_swap_teams:
        # print(team_idx)
        schedule[team_idx][round1_idx], schedule[team_idx][round2_idx] = \
        schedule[team_idx][round2_idx], schedule[team_idx][round1_idx]

    return schedule


# # Example usage
# schedule = [
#     # [6, -2, 2, 3, -5, -4, -3, 5, 4, -6],  # Team 1
#     # [5, 1, -1, -5, 4, 3, 6, -4, -6, -3],  # Team 2
#     # [-4, 5, 4, -1, 6, -2, 1, -6, -5, 2],  # Team 3
#     # [3, 6, -3, -6, -2, 1, 5, 2, -1, -5],  # Team 4
#     # [-2, -3, 6, 2, 1, -6, -4, -1, 3, 4],  # Team 5
#     # [-1, -4, -5, 4, -3, 5, -2, 3, 2, 1],  # Team 6
#     [4, -3, 2, -4, 3, -2],  # Team 1
#     [3, -4, -1, -3, 4, 1],  # Team 2
#     [-2, 1, 4, 2, -1, -4],  # Team 3
#     [-1, 2, -3, 1, -2, 3]   # Team 4
# ]


# r1 = 1  # Day 1
# r2 = 2  # Day 2 (index 0)
# team_idx = 2  # Team 1
