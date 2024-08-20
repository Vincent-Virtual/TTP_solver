import math
import xml.etree.ElementTree as ET

def read_xml_and_create_distance_matrix(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the maximum team ID to determine the size of the distance matrix
    max_team_id = 0
    for distance in root.findall('.//distance'):
        team1_id = int(distance.get('team1'))
        team2_id = int(distance.get('team2'))
        max_team_id = max(max_team_id, team1_id, team2_id)

    num_teams = max_team_id + 1

    # Initialize the distance matrix
    distance_matrix = [[0 for _ in range(num_teams)] for _ in range(num_teams)]

    # Populate the distance matrix
    for distance in root.findall('.//distance'):
        team1 = int(distance.get('team1'))
        team2 = int(distance.get('team2'))
        dist = int(distance.get('dist'))
        distance_matrix[team1][team2] = dist
        distance_matrix[team2][team1] = dist  # Assuming symmetric distances

    return distance_matrix


def calculate_total_distance(schedule, distance_matrix):
    total_distance = 0
    num_teams = len(schedule)

    for team_idx, team_schedule in enumerate(schedule):
        current_location = team_idx  # Teams start at their home location
        for game in team_schedule:
            if game < 0:  # Away game
                opponent_idx = abs(game) - 1
                # Add distance from the current location to the away game location
                total_distance += distance_matrix[current_location][opponent_idx]
                current_location = opponent_idx  # Update current location to this away game location
            else:  # Home game
                if current_location != team_idx:  # If not already at home, add distance to return home
                    total_distance += distance_matrix[current_location][team_idx]
                    current_location = team_idx  # Update location back to home

        # Ensure return to home after the last game if it was away
        if current_location != team_idx:
            total_distance += distance_matrix[current_location][team_idx]
            
    return total_distance

# def output_schedule(schedule):
#     for team_index, team_schedule in enumerate(schedule, start=1):
#         print(f"Team {team_index}'s Schedule: {team_schedule}")

def output_schedule(schedule):
    for team_index, team_schedule in enumerate(schedule, start=1):
        # Adjust the team index formatting to include an extra space for single-digit numbers
        if team_index < 10:
            team_str = f"Team  {team_index}'s Schedule: "  # Two spaces after 'Team' for single-digit team numbers
        else:
            team_str = f"Team {team_index}'s Schedule: "  # One space after 'Team' for double-digit team numbers
        
        # Format each game in the schedule to occupy exactly 3 characters
        formatted_schedule = " ".join(f"{game: 3d}" for game in team_schedule)
        print(f"{team_str}[{formatted_schedule}]")


def count_violations(schedule):
    at_most_violations = 0
    no_repeater_violations = 0

    # Check the "at most" constraint for each team
    for team_schedule in schedule:
        # Track consecutive home or away games
        consecutive_home = 0
        consecutive_away = 0

        # Check for consecutive home or away games
        for game in team_schedule:
            if game > 0:  # Home game
                consecutive_home += 1
                consecutive_away = 0
            else:  # Away game
                consecutive_away += 1
                consecutive_home = 0

            # Check if there's a violation of the 'at most' constraint
            if consecutive_home > 3 or consecutive_away > 3:
                at_most_violations += 1

    # Check the "no repeater" constraint for each team
    for team_schedule in schedule:
        # Check for consecutive games against the same team
        for i in range(len(team_schedule) - 1):
            if abs(team_schedule[i]) == abs(team_schedule[i + 1]):
                no_repeater_violations += 1

    # Total violations is the sum of violations from both constraints
    total_violations = at_most_violations + no_repeater_violations
    return total_violations

def cost_with_violations(schedule, distance_matrix, weight = 3000):
    violations = count_violations(schedule)

    if violations == 0:
        return calculate_total_distance(schedule, distance_matrix)
    
    return math.sqrt(calculate_total_distance(schedule, distance_matrix)**2 + (weight*violations)**2)



##Neighbourhood swaps

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

def partial_swap_round(schedule, team1_idx, team2_idx, team3_idx, team4_idx, i, j):
    pass

def partial_swap_team(schedule, team1_idx, team2_idx, i):
    pass
