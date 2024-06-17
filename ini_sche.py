import random

# alternating home and away for each rotation
def generate_round_robin_schedule(num_teams):
    if num_teams % 2 != 0:
        raise ValueError("Number of teams must be even for this method.")
    
    # Initialize the schedule
    schedule = [[] for _ in range(2 * (num_teams - 1))]
    
    # List of teams using zero-based indexing
    # teams = list(range(num_teams))
    
    # Generate each round of matches following the rotation technique
    # decide the 'stabbing' line, then 'parallel lines'

    for round in range(num_teams - 1):
        ## round indexes the stabbing line
        round_matches = []
        # starting_team = round + 1


        for i in range(num_teams // 2):
        ## i indexed how much left and right from the stabbing line
            if i == 0:
                # Alternate home and away for the last team
                if round % 2 == 0:
                    round_matches.append((round+1, num_teams))
                else:
                    round_matches.append((num_teams, round+1))

                # round_matches.append((round + 1, num_teams))
                continue
            
            ## decide the left and right end point for each parallel line
            left = (round - i + num_teams-1) % (num_teams-1) + 1
            right = (round + i) % (num_teams-1) + 1
            
                
            ## Alternate btw home and away for each team
            if i % 2 == 0:
                round_matches.append((left, right))
            else:
                round_matches.append((right, left))
        
        # Create a new list with reversed tuples
        mirrored_matches = [(b, a) for a, b in round_matches]

        # Add the round to the schedule
        schedule[round] = round_matches

        schedule[round + num_teams -1] = mirrored_matches
    
    return schedule


# ## original rotation
# def generate_round_robin_schedule(num_teams):
#     if num_teams % 2 != 0:
#         raise ValueError("Number of teams must be even for this method.")
    
#     # Initialize the schedule
#     schedule = [[] for _ in range(2 * (num_teams - 1))]
    
#     # List of teams using zero-based indexing
#     # teams = list(range(num_teams))
    
#     # Generate each round of matches following the rotation technique
#     # decide the 'stabbing' line, then 'parallel lines'

#     for round in range(num_teams - 1):
#         ## round indexes the stabbing line
#         round_matches = []
#         # starting_team = round + 1


#         for i in range(num_teams // 2):
#         ## i indexed how much left and right from the stabbing line

#             if i == 0: ## the 'stabbing' line
                
#                 if random.choice([True, False]):
#                     round_matches.append((round+1, num_teams))

#                 else:
#                     round_matches.append((num_teams, round + 1))
#                 # round_matches.append((round + 1, num_teams))
#                 continue
            
#             ## decide the left and right end point for each parallel line
#             left = (round - i + num_teams-1) % (num_teams-1) + 1
#             right = (round + i) % (num_teams-1) + 1
            
#             if random.choice([True, False]):
#                     round_matches.append((left, right))

#             else:
#                 round_matches.append((right, left))
            

#         # Create a new list with reversed tuples
#         mirrored_matches = [(b, a) for a, b in round_matches]

#         # Add the round to the schedule
#         schedule[round] = round_matches

#         schedule[round + num_teams - 1] = mirrored_matches
    
#     return schedule

def generate_team_centric_schedule(num_teams):
    # Generate the round-robin schedule as before
    schedule = generate_round_robin_schedule(num_teams)
    
    # Initialize the team-centric schedule format
    team_schedules = {team: [] for team in range(1, num_teams + 1)}
    
    # Populate the team-centric schedule
    for round_matches in schedule:
        for home, away in round_matches:
            team_schedules[home].append(away)  # Home game for 'home' team
            team_schedules[away].append(-home)  # Away game for 'away' team, indicated with a negative sign
    
    # Convert the dictionary to a list for a final output, maintaining the team order
    team_schedules_list = [team_schedules[team] for team in sorted(team_schedules)]
    
    return team_schedules_list

