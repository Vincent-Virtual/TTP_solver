from xml.etree import ElementTree as ET
from common import output_schedule, calculate_total_distance

import numpy as np

def parse_ttp_solution(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the <Games> element
    games = root.find('Games')
    if games is None:
        print("Error: <Games> element not found in the XML.")
        return

    # Initialize variables to track the largest slot number
    max_slot = -1

    # Process each <ScheduledMatch> inside <Games>
    for match in games.findall('ScheduledMatch'):
        # away = int(match.get('away')) + 1  # Convert to 1-based index
        # home = int(match.get('home')) + 1
        slot = int(match.get('slot'))

        # Print extracted fields for debugging
        # print(f"Home: {home}, Away: {away}, Slot: {slot}")

        # Update the largest slot number
        max_slot = max(max_slot, slot)

    # Determine the number of teams
    num_teams = (max_slot + 1) // 2 + 1

    # Initialize schedule for the determined number of teams
    schedule = [[] for _ in range(num_teams)]

    # Process each <ScheduledMatch> inside <Games> again to fill the schedule
    for match in games.findall('ScheduledMatch'):
        away = int(match.get('away')) + 1  # Convert to 1-based index
        home = int(match.get('home')) + 1
        slot = int(match.get('slot'))

        # Resize the inner lists if necessary
        while len(schedule[home-1]) <= slot:
            schedule[home-1].append(0)
        while len(schedule[away-1]) <= slot:
            schedule[away-1].append(0)

        # Set the schedule for home and away
        schedule[home-1][slot] = away  # Home team has a positive number
        schedule[away-1][slot] = -home  # Away team has a negative number

    arr = [[1 for _ in range(10)] for _ in range(num_teams)]
    # print(calculate_total_distance(schedule, arr))
    output_schedule(schedule)

def parse_schedule_to_array(schedule_str: str):
    """
    This function takes a string with team schedules formatted in the pattern seen earlier
    and returns a 2D array (as a list of lists) representing the schedules.
    """
    lines = schedule_str.strip().splitlines()
    num_teams = len(lines)
    schedule = []
    
    for line in lines:
        # Extract the portion between square brackets and convert it to a list of integers
        start_idx = line.index('[') + 1
        end_idx = line.index(']')
        team_schedule = line[start_idx:end_idx].split()
        schedule_list = [int(num) for num in team_schedule]  # Ensuring conversion to integers
        # print(type(schedule_list[0]))
        schedule.append(schedule_list)
    
    return schedule
    # arr = [[1 for _ in range((num_teams-1)*2)] for _ in range(num_teams)]
    # print(type(arr[0][0]))
    # print(arr)
    # print(schedules)
    # print(calculate_total_distance(schedule, arr))



# parse_ttp_solution("./Solutions/CON10Sol.xml")
schedule_str = """
Team  1's Schedule: [  4  10   2  -4 -10  -6   9   7   5  -7  -3  -5   6   3   8  -9  -2  -8]
Team  2's Schedule: [ -9  -5  -1   3   9  10  -3  -4 -10   5   4   7  -8  -7  -6   8   1   6]
Team  3's Schedule: [  6   7   9  -2  -6  -7   2  -5  -8  -9   1   8 -10  -1  -4   5  10   4]
Team  4's Schedule: [ -1  -8 -10   1   5   8  -5   2   9  10  -2  -6   7   6   3  -7  -9  -3]
Team  5's Schedule: [  7   2   6  -7  -4  -9   4   3  -1  -2  -6   1   9   8 -10  -3  -8  10]
Team  6's Schedule: [ -3  -9  -5   9   3   1  -8 -10  -7   8   5   4  -1  -4   2  10   7  -2]
Team  7's Schedule: [ -5  -3  -8   5   8   3 -10  -1   6   1  10  -2  -4   2   9   4  -6  -9]
Team  8's Schedule: [ 10   4   7 -10  -7  -4   6   9   3  -6  -9  -3   2  -5  -1  -2   5   1]
Team  9's Schedule: [  2   6  -3  -6  -2   5  -1  -8  -4   3   8  10  -5 -10  -7   1   4   7]
Team 10's Schedule: [ -8  -1   4   8   1  -2   7   6   2  -4  -7  -9   3   9   5  -6  -3  -5]"""

schedule = parse_schedule_to_array(schedule_str)
