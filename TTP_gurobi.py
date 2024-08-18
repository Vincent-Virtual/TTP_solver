import gurobipy as gp
from gurobipy import GRB
from common import read_xml_and_create_distance_matrix

import json

# with open('schedule.json', 'r') as file:
#     schedule = json.load(file)


file_path = './Instances/CON4.xml'
dij = read_xml_and_create_distance_matrix(file_path)

n = len(dij)  # Example number of teams


# Initialize the model
m = gp.Model()

# Define variables xijk, ytij, zijk

## if team i plays away against team j in round k
xijk = m.addVars(n, n, 2*n-2, vtype=GRB.BINARY, name="xijk")

## if team t travels from team i's place to team j's place ever
ytij = m.addVars(n, n, n, vtype=GRB.BINARY, name="ytij")


zijk = m.addVars(n, n, 2*n-2, vtype=GRB.BINARY, name="zijk")


xijk_tilde = m.addVars(n, n, 2*n-2, vtype=GRB.BINARY, name="xijk_tilde")

# Set the variables according to the schedule
# for i in range(n):
#     for k in range(2*n-2):
#         if k < len(schedule[i]):  # Ensure we don't go out of index
#             opponent = schedule[i][k]
#             j = abs(opponent) - 1  # Convert opponent to zero-based index
#             if opponent < 0:
#                 # If opponent is negative, team i is playing away
#                 xijk_tilde[i, j, k].setAttr("UB", 1)  # Ensure the upper bound is 1 (since it's already a binary var)
#                 xijk_tilde[i, j, k].setAttr("LB", 1)  # Lock this variable to 1 (team i plays away at team j)
#             else:
#                 # If opponent is positive, ensure team i is not playing away at team j
#                 xijk_tilde[i, j, k].setAttr("UB", 0)  # Lock this variable to 0
#                 xijk_tilde[i, j, k].setAttr("LB", 0)  # Ensure the lower bound is 0

initial_moves = gp.quicksum(dij[i][j] * xijk[i, j, 0] for i in range(n) for j in range(n))

intermediate_moves = gp.quicksum(dij[i][j] * ytij[t, i, j] for t in range(n) for i in range(n) for j in range(n))

back_moves = gp.quicksum(dij[j][i] * xijk[i, j, 2*n-3] for i in range(n) for j in range(n))

# Set the objective function

# obj = initial_moves + intermediate_0 + intermediate_1 + intermediate_2 + intermediate_3 + back_moves
obj = initial_moves + intermediate_moves + back_moves

m.setObjective(obj, GRB.MINIMIZE)

# Add constraints

# m.addConstrs((xijk[i, i, k] + xijk[j, i, k] == xijk_tilde[i, j, k] + xijk_tilde[j, i, k] for i in range(n) for j in range(n) for k in range(2*n-2)), name = "C12")

# a team never plays against itself
m.addConstrs((xijk[i, i, k] == 0 for i in range(n) for k in range(2*n - 2)), name = "C2")

# each team to play exactly one match per day (either home or away)
m.addConstrs((gp.quicksum(xijk[i, j, k] + xijk[j, i, k] for j in range(n)) == 1 for i in range(n) for k in range(2*n-2)), name="C3")

# every team plays each other team once away and once at home over the 2n − 2 days
m.addConstrs((gp.quicksum(xijk[i, j, k] for k in range(2*n-2)) == 1 for i in range(n) for j in range(n) if i != j), name="C4")


# Constraint (5): Ensure home stands and road trips have a length of at most 3
m.addConstrs((gp.quicksum(xijk[i, j, k + l] for l in range(4) for j in range(n)) <= 3 
                  for i in range(n) for k in range(2*n - 2 - 3)), name="C5")

# Constraint (6): Ensure home stands and road trips have a length of at most 3
m.addConstrs((gp.quicksum(xijk[i, j, k + l] for l in range(4) for i in range(n)) <= 3 
                  for j in range(n) for k in range(2*n - 2 - 3)), name="C6")


# no-repeater constraint
m.addConstrs((xijk[i, j, k] + xijk[j, i, k] + xijk[i, j, k+1] + xijk[j, i, k+1]  <= 1 for i in range(n) for j in range(n) for k in range(2*n - 3)), name="C7")

# driving behavior of the teams
m.addConstrs((zijk[j, j, k] == gp.quicksum(xijk[i, j, k] for i in range(n)) for j in range(n) for k in range(2*n-2)), name="C8")
m.addConstrs((zijk[i, j, k] == xijk[i, j, k] for i in range(n) for j in range(n) if i != j for k in range(2*n-2) ), name="C9")
m.addConstrs((ytij[t, i, j] >= zijk[t, i, k] + zijk[t, j, k+1] - 1 for t in range(n) for i in range(n) for j in range(n) for k in range(2*n-3) ), name="C10")



# Optimize the model
# Set the number of solutions to be stored in the solution pool to 1
m.setParam('PoolSolutions', 1)

# Set pool search mode to only look for the best solution
m.setParam('PoolSearchMode', 0)
m.optimize()

# Output the results
if m.status == GRB.OPTIMAL:
    print("Optimal solution found")
    # for v in m.getVars():
    #     if v.x > 0:
    #         print(f"{v.varName}: {v.x}")
    
    # print(initial_moves.getValue())

    # print(back_moves.getValue())
else:
    print("No optimal solution found")

# for v in m.getVars():
#     print('%s %g' % (v.VarName, v.X))
# print("obj value is ", m.ObjVal)
