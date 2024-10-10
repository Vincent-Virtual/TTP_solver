def partial_swap_team(schedule, team1_idx, team2_idx, start_round, return_pivot_round_idx = False):
    num_rounds = len(schedule[0])
    # print(start_round, len(schedule[team1_idx]))
    # print(len(schedule[team1_idx]))
    # print(start_round)

    if abs(schedule[team1_idx][start_round]) == team2_idx + 1:
        if return_pivot_round_idx:
            return schedule, -1     # return pivot_team_idx as -1 to refer to not valid swap
        return schedule


    opponent1 = schedule[team1_idx][start_round]
    opponent2 = schedule[team2_idx][start_round]
    visited_rounds = set()
    visited_rounds.add(start_round)

    # checking_team_idx = team1_idx
    checking_opponent = opponent2

    ## Check if finally the opponent to reset coincides with oppo1 who triggers everything
    while checking_opponent != opponent1:
        for r in range(num_rounds):
            ## check the potential duplicate entry with its round in team1's schedule 
            # after geting "checking opponent" from team2's schedule
            if schedule[team1_idx][r] == checking_opponent:
                ## update the checking oppo in team2's schedule
                checking_opponent = schedule[team2_idx][r]
                visited_rounds.add(r)
                # input()
                # print(r, checking_opponent)
                break
    
    smallest_idx = min(visited_rounds)

    # print("ps team")
    for r in visited_rounds:
        # Swap the games except the ones they play against each other
        schedule[team1_idx][r], schedule[team2_idx][r] = schedule[team2_idx][r], schedule[team1_idx][r]

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

    if return_pivot_round_idx:
        return schedule, smallest_idx
    
    return schedule
    

# schedule = [
#     [6, -2, 2, 3, -5, -4, -3, 5, 4, -6],  # Team 1
#     [5, 1, -1, -5, 4, 3, 6, -4, -6, -3],  # Team 2
#     [-4, 5, 4, -1, 6, -2, 1, -6, -5, 2],  # Team 3
#     [3, 6, -3, -6, -2, 1, 5, 2, -1, -5],  # Team 4
#     [-2, -3, 6, 2, 1, -6, -4, -1, 3, 4],  # Team 5
#     [-1, -4, -5, 4, -3, 5, -2, 3, 2, 1],  # Team 6
# #     [4, -3, 2, -4, 3, -2],  # Team 1
# #     [3, -4, -1, -3, 4, 1],  # Team 2
# #     [-2, 1, 4, 2, -1, -4],  # Team 3
# #     [-1, 2, -3, 1, -2, 3]   # Team 4
# ]


# team1_idx = 1  # Index of team 1 in the schedule
# team2_idx = 2  # Index of team 2 in the schedule
# start_round = 2  # For example, swap the second round (index 1)

# schedule = partial_swap_team(schedule, team1_idx, team2_idx, start_round)
# output_schedule(schedule)

# # print(schedule[team1_idx])  # Updated schedule for team1
# # print(schedule[team2_idx])  # Updated schedule for team2
