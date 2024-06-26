import json

def find_pattern_in_schedule(schedule):
    num_teams = len(schedule)
    num_rounds = len(schedule[0])
    
    # Convert the schedule into a list of sets of games per round
    rounds = [set() for _ in range(num_rounds)]
    for i in range(num_teams):
        for j in range(num_rounds):
            opponent = schedule[i][j]
            if opponent > 0:
                game = (i+1, opponent) if i+1 < opponent else (opponent, i+1)
                rounds[j].add(game)

    # Search for the pattern across rounds
    for i in range(num_rounds):
        for j in range(i + 1, num_rounds):
            round_i_games = rounds[i]
            round_j_games = rounds[j]
            
            # Check every combination of teams to find the pattern
            for a in range(1, num_teams + 1):
                for b in range(a + 1, num_teams + 1):
                    for c in range(1, num_teams + 1):
                        if c == a or c == b:
                            continue
                        for d in range(c + 1, num_teams + 1):
                            if d == a or d == b:
                                continue
                            
                            ab_cd_i = {(a, b), (c, d)} <= round_i_games
                            ac_bd_j = {(a, c), (b, d)} <= round_j_games
                            ab_cd_j = {(a, b), (c, d)} <= round_j_games
                            ac_bd_i = {(a, c), (b, d)} <= round_i_games
                            
                            if (ab_cd_i and ac_bd_j) or (ab_cd_j and ac_bd_i):
                                return True
    
    return False

with open('schedule.json', 'r') as file:
    schedule = json.load(file)

result = find_pattern_in_schedule(schedule)
print("Pattern found:", result)
