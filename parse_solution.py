from xml.etree import ElementTree as ET
from common import output_schedule

# Sample XML data
xml_data = """
<Games>
    <ScheduledMatch home="0" away="2" slot="0"/>
    <ScheduledMatch home="0" away="4" slot="1"/>
    <ScheduledMatch home="0" away="1" slot="5"/>
    <ScheduledMatch home="0" away="5" slot="6"/>
    <ScheduledMatch home="0" away="3" slot="7"/>
    <ScheduledMatch home="1" away="3" slot="0"/>
    <ScheduledMatch home="1" away="5" slot="1"/>
    <ScheduledMatch home="1" away="0" slot="2"/>
    <ScheduledMatch home="1" away="2" slot="6"/>
    <ScheduledMatch home="1" away="4" slot="7"/>
    <ScheduledMatch home="2" away="3" slot="1"/>
    <ScheduledMatch home="2" away="4" slot="2"/>
    <ScheduledMatch home="2" away="0" slot="3"/>
    <ScheduledMatch home="2" away="5" slot="7"/>
    <ScheduledMatch home="2" away="1" slot="8"/>
    <ScheduledMatch home="3" away="1" slot="3"/>
    <ScheduledMatch home="3" away="2" slot="4"/>
    <ScheduledMatch home="3" away="5" slot="5"/>
    <ScheduledMatch home="3" away="4" slot="8"/>
    <ScheduledMatch home="3" away="0" slot="9"/>
    <ScheduledMatch home="4" away="5" slot="0"/>
    <ScheduledMatch home="4" away="0" slot="4"/>
    <ScheduledMatch home="4" away="2" slot="5"/>
    <ScheduledMatch home="4" away="3" slot="6"/>
    <ScheduledMatch home="4" away="1" slot="9"/>
    <ScheduledMatch home="5" away="3" slot="2"/>
    <ScheduledMatch home="5" away="4" slot="3"/>
    <ScheduledMatch home="5" away="1" slot="4"/>
    <ScheduledMatch home="5" away="0" slot="8"/>
    <ScheduledMatch home="5" away="2" slot="9"/>
</Games>
"""

# Parse the XML
root = ET.fromstring(xml_data)

# Initialize schedule for 6 teams (assuming team indices in XML are 0-based and need to be 1-based)
num_teams = 6
schedule = [[] for _ in range(num_teams)]

# Process each match in the XML
for match in root:
    away = int(match.get('away')) + 1  # Convert to 1-based index
    home = int(match.get('home')) + 1
    slot = int(match.get('slot'))
    
    # Resize the inner lists if necessary (Pythonic way to handle lists growing dynamically)
    while len(schedule[home-1]) <= slot:
        schedule[home-1].append(0)
    while len(schedule[away-1]) <= slot:
        schedule[away-1].append(0)
    
    # Set the schedule for home and away
    schedule[home-1][slot] = away  # Home team has a positive number
    schedule[away-1][slot] = -home  # Away team has a negative number

# Print the schedule in the desired format
output_schedule(schedule)
