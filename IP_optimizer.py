# Given schedule as a 2D list
schedule = [
    [-4,  6,  5, -3, -6, -2,  3, -5,  2,  4],  # Team 1's Schedule
    [ 3,  5, -4, -6, -5,  1,  6,  4, -1, -3],  # Team 2's Schedule
    [-2, -4, -6,  1,  4, -5, -1,  6,  5,  2],  # Team 3's Schedule
    [ 1,  3,  2, -5, -3,  6,  5, -2, -6, -1],  # Team 4's Schedule
    [ 6, -2, -1,  4,  2,  3, -4,  1, -3, -6],  # Team 5's Schedule
    [-5, -1,  3,  2,  1, -4, -2, -3,  4,  5]   # Team 6's Schedule
]

# Initialize list to store away games
away_games = []

# Iterate over each team's schedule
for team_i, games in enumerate(schedule, start=1):
    for round_k, opponent in enumerate(games, start=1):
        if opponent < 0:  # away game
            team_j = abs(opponent)
            away_games.append((team_i, team_j, round_k))

# Print the results
for i, j, k in away_games:
    print(f"x_{i}{j}{k} = 1")
