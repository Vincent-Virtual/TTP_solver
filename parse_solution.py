from xml.etree import ElementTree as ET
from common import output_schedule

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

    print(max_slot)
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

    output_schedule(schedule)
parse_ttp_solution("./Solutions/CIRC12_Lim2006.xml")