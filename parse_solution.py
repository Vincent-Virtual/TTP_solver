from xml.etree import ElementTree as ET
from common import *
from neighbourhood import *

import sys


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

    return schedule
    

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
    
    # return schedule
    arr = [[1 for _ in range((num_teams-1)*2)] for _ in range(num_teams)]
    # print(type(arr[0][0]))
    # print(arr)
    # print(schedules)
    # print(calculate_total_distance(schedule, arr))
    return schedule



# filename = ""
# if len(sys.argv) > 1:
#     filename = sys.argv[1]  # sys.argv[1] is the first command-line argument

# else:
#     print("No arguments provided.")
#     sys.exit(1)


# file_path = './Instances/{}.xml'.format(filename)

# distance_matrix = read_xml_and_create_distance_matrix(file_path)

# schedule = parse_ttp_solution("./Solutions/CIRC/CIRC10_Sol_Uthus.xml")
schedule_str = '''
Team  1's Schedule: [  5   2   6  -3  -4  -6   3   4  -2  -5]
Team  2's Schedule: [ -3  -1  -5   4  -6   5  -4   6   1   3]
Team  3's Schedule: [  2  -6   4   1   5  -4  -1  -5   6  -2]
Team  4's Schedule: [ -6   5  -3  -2   1   3   2  -1  -5   6]
Team  5's Schedule: [ -1  -4   2   6  -3  -2  -6   3   4   1]
Team  6's Schedule: [  4   3  -1  -5   2   1   5  -2  -3  -4]'''

schedule = parse_schedule_to_array(schedule_str)
output_schedule(schedule)
print()
schedule = partial_swap_team(schedule, 1, 3, 0)
output_schedule(schedule)
print()
schedule = swap_home(schedule, 2, 3)
output_schedule(schedule)
print()
schedule = partial_swap_team(schedule, 2, 3, 1)
output_schedule(schedule)
print()
# schedule = partial_swap_team(schedule, 1, 2, 4)
# output_schedule(schedule)
# print()
# schedule = partial_swap_team(schedule, 1, 2, 5)
# output_schedule(schedule)
# output_schedule_with_distances(schedule, distance_matrix)

# print(calculate_total_distance(schedule, distance_matrix))
# print(count_violations(schedule))

# for row in distance_matrix:
#     print(row)