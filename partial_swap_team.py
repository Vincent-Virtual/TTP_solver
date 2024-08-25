def partial_swap_team(schedule, team1_idx, team2_idx, start_round):
    # print(start_round, len(schedule[team1_idx]))
    # print(len(schedule[team1_idx]))
    # print(start_round)
    schedule[team1_idx][start_round]
    if abs(schedule[team1_idx][start_round]) == team2_idx + 1:
        return schedule


    def find_conflict_loop(schedule, team1_idx, team2_idx, start_round):
        loop_indices = []
        visited_rounds = set()
        
        current_round = start_round
        while current_round not in visited_rounds:
            print("in while loop")
            visited_rounds.add(current_round)
            loop_indices.append(current_round)
            
            # Get the current opponents for both teams in this round
            current_opponent_team1 = schedule[team1_idx][current_round]
            current_opponent_team2 = schedule[team2_idx][current_round]
            
            # Find the next round where the current opponent of team1 is scheduled to play against team2
            # or the current opponent of team2 is scheduled to play against team1
            if current_opponent_team1 in schedule[team2_idx]:
                next_round = schedule[team2_idx].index(current_opponent_team1)
            else:
                next_round = schedule[team1_idx].index(current_opponent_team2)
            
            current_round = next_round
        
        return loop_indices

    def swap_opponents(schedule, team1_idx, team2_idx, round):
        # Swap the opponents of team1 and team2 in the specified round
        temp = schedule[team1_idx][round]
        schedule[team1_idx][round] = schedule[team2_idx][round]
        schedule[team2_idx][round] = temp
    
    # Find the rounds that need to be swapped
    loop_indices = find_conflict_loop(schedule, team1_idx, team2_idx, start_round)
    
    # Perform the swaps for all the rounds in the loop
    for i in loop_indices:
        swap_opponents(schedule, team1_idx, team2_idx, i)

    return schedule



# team1_schedule = [3, 5, 1, -6, -5, -4, 6, 4, -1, -3]
# team2_schedule = [-2, -4, -5, 1, 4, -6, -1, 6, 5, 2]

# schedule = [team1_schedule, team2_schedule]
# team1_idx = 0  # Index of team 1 in the schedule
# team2_idx = 1  # Index of team 2 in the schedule
# start_round = 1  # For example, swap the second round (index 1)

# partial_swap_team(schedule, team1_idx, team2_idx, start_round)

# print(schedule[team1_idx])  # Updated schedule for team1
# print(schedule[team2_idx])  # Updated schedule for team2
