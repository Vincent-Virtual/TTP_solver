##Neighbourhood swaps

from partial_swap_round import partial_swap_round

def swap_round(schedule, round1_idx, round2_idx):
    """
    Swaps two rounds in the tournament schedule.
    
    Args:
    schedule (list of lists): The tournament schedule where each inner list represents a team's schedule.
    
    Returns:
    list of lists: The updated tournament schedule after swapping two rounds.
    """

    # print(1)
    num_rounds = len(schedule)  # Assuming all teams play the same number of rounds
    
    
    # Swap the selected rounds for all teams
    for team_schedule in schedule:
        # Swap the games in round1_idx and round2_idx for each team
        team_schedule[round1_idx], team_schedule[round2_idx] = team_schedule[round2_idx], team_schedule[round1_idx]
    
    return schedule


def swap_home(schedule, team1_idx, team2_idx):
    """
    Randomly selects two different teams and swaps their home and away games against each other
    in the tournament schedule.
    """

    # print(2)
    num_teams = len(schedule)
    # team1_idx, team2_idx = random.sample(range(num_teams), 2)  # Ensure two distinct teams are selected
    # print(team1_idx, team2_idx)

    # Convert team indices to 1-based indexing to match schedule representation
    team1_game = team2_idx + 1
    team2_game = -(team1_idx + 1)

    # Find the positions of the games to swap for both teams
    team1_positions = [i for i, game in enumerate(schedule[team1_idx]) if abs(game) == team1_game]
    team2_positions = [i for i, game in enumerate(schedule[team2_idx]) if abs(game) == abs(team2_game)]

    # Perform the swap
    if team1_positions and team2_positions:
        # Swap the first game
        schedule[team1_idx][team1_positions[0]] *= -1
        schedule[team2_idx][team2_positions[0]] *= -1

        # Swap the second game (if exists)
        if len(team1_positions) > 1 and len(team2_positions) > 1:
            schedule[team1_idx][team1_positions[1]] *= -1
            schedule[team2_idx][team2_positions[1]] *= -1

    return schedule


def swap_team(schedule, team1_idx, team2_idx):  ## should fix after swapping
    
#     """
#     Swaps the schedules of two randomly selected teams except for the games
#     between the two teams.
#     """

    # print(3)
    num_teams = len(schedule)
    # team1_idx, team2_idx = random.sample(range(num_teams), 2)  # Randomly select two different teams
    # print(team1_idx, team2_idx)

    # Find the games between the selected teams and preserve them
    for i in range(len(schedule[0])):
        if abs(schedule[team1_idx][i]) == team2_idx + 1:
            # These are the games between team1 and team2;
            schedule[team1_idx][i] = - schedule[team1_idx][i]
            schedule[team2_idx][i] = - schedule[team2_idx][i]
            continue
        
        # Swap the games except the ones they play against each other
        schedule[team1_idx][i], schedule[team2_idx][i] = schedule[team2_idx][i], schedule[team1_idx][i]

        # resolve mismatches in the round after swapping 2 teams
        affected_team1_idx = abs(schedule[team1_idx][i]) - 1
        affected_team2_idx = abs(schedule[team2_idx][i]) - 1
        # print(affected_team1, affected_team2)

        schedule[affected_team1_idx][i], schedule[affected_team2_idx][i] = \
        schedule[affected_team2_idx][i], schedule[affected_team1_idx][i]

        if schedule[team1_idx][i] > 0:
            schedule[affected_team1_idx][i] = -abs(schedule[affected_team1_idx][i])
        else:
            schedule[affected_team1_idx][i] = abs(schedule[affected_team1_idx][i])

        if schedule[team2_idx][i] > 0:
            schedule[affected_team2_idx][i] = -abs(schedule[affected_team2_idx][i])
        else:
            schedule[affected_team2_idx][i] = abs(schedule[affected_team2_idx][i])
    return schedule

