import gurobipy as gp
from gurobipy import GRB
from common import read_xml_and_create_distance_matrix

# Assuming we have the distance matrix dij of n teams
# n = 5  # Example number of teams
# dij = [[0, 2, 9, 10, 1],
#        [1, 0, 6, 4, 5],
#        [3, 7, 0, 8, 2],
#        [6, 4, 3, 0, 7],
#        [4, 2, 5, 7, 0]]  # Example distance matrix

file_path = './Instances/CIRC4.xml'
dij = read_xml_and_create_distance_matrix(file_path)

n = len(dij)  # Example number of teams


# Initialize the model
m = gp.Model()

# Define variables xijk, ytij, zijk
xijk = m.addVars(n, n, 2*n-2, vtype=GRB.BINARY, name="xijk")
ytij = m.addVars(n, n, n, vtype=GRB.BINARY, name="ytij")
zijk = m.addVars(n, n, 2*n-2, vtype=GRB.BINARY, name="zijk")

initial_moves = gp.quicksum(dij[i][j] * xijk[i, j, 0] for i in range(n) for j in range(n))

intermediate_moves = gp.quicksum(dij[i][j] * ytij[t, i, j] for t in range(n) for i in range(n) for j in range(n))
# intermediate_0 = gp.quicksum(dij[0][j] * ytij[t, 0, j] for t in range(n) for j in range(n)) + \
#                  gp.quicksum(dij[i][0] * ytij[t, i, 0] for t in range(n) for i in range(n))

# intermediate_1 = gp.quicksum(dij[1][j] * ytij[t, 1, j] for t in range(n) for j in range(n)) + \
#                  gp.quicksum(dij[i][1] * ytij[t, i, 1] for t in range(n) for i in range(n))

# intermediate_2 = gp.quicksum(dij[2][j] * ytij[t, 2, j] for t in range(n) for j in range(n)) + \
#                  gp.quicksum(dij[i][2] * ytij[t, i, 2] for t in range(n) for i in range(n))

# intermediate_3 = gp.quicksum(dij[3][j] * ytij[t, 3, j] for t in range(n) for j in range(n)) + \
                #  gp.quicksum(dij[i][3] * ytij[t, i, 3] for t in range(n) for i in range(n))

intermediate_0 = gp.quicksum(dij[i][j] * ytij[0, i, j] for i in range(n) for j in range(n))

intermediate_1 = gp.quicksum(dij[i][j] * ytij[1, i, j] for i in range(n) for j in range(n))

intermediate_2 = gp.quicksum(dij[i][j] * ytij[2, i, j] for i in range(n) for j in range(n))

intermediate_3 = gp.quicksum(dij[i][j] * ytij[3, i, j] for i in range(n) for j in range(n))

back_moves = gp.quicksum(dij[j][i] * xijk[i, j, 2*n-3] for i in range(n) for j in range(n))

# Set the objective function
# obj = gp.quicksum(dij[i][j] * xijk[i, j, 0] for i in range(n) for j in range(n)) \
#       + gp.quicksum(dij[i][j] * ytij[t, i, j] for t in range(n) for i in range(n) for j in range(n)) \
#       + gp.quicksum(dij[j][i] * xijk[i, j, 2*n-3] for i in range(n) for j in range(n))

obj = initial_moves + intermediate_0 + intermediate_1 + intermediate_2 + intermediate_3 + back_moves
# obj = initial_moves + intermediate_moves + back_moves

m.setObjective(obj, GRB.MINIMIZE)

# Add constraints

# a team never plays against itself
# m.addConstrs((gp.quicksum(xijk[i, j, k] for i in range(n) for j in range(n) for k in range(1, 2*n-2) if i == j) == 0), name="C2")

m.addConstrs(xijk[i, i, k] == 0 for i in range(n) for k in range(2*n - 2))

# each team to play exactly one match per day (either home or away)
m.addConstrs((gp.quicksum(xijk[i, j, k] + xijk[j, i, k] for j in range(n)) == 1 for i in range(n) for k in range(2*n-2)), name="C3")

# every team plays each other team once away and once at home over the 2n − 2 days
m.addConstrs((gp.quicksum(xijk[i, j, k] for k in range(2*n-2)) == 1 for i in range(n) for j in range(n) if i != j), name="C4")


# Constraint (5): Ensure home stands and road trips have a length of at most 3
m.addConstrs((gp.quicksum(xijk[i, j, k + l] for l in range(4) for j in range(n)) <= 3 
                  for i in range(n) for k in range(2*n - 2 - 3)), name="C5")

# Constraint (5): Ensure home stands and road trips have a length of at most 3
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
    for v in m.getVars():
        if v.x > 0:
            print(f"{v.varName}: {v.x}")
    
    print(initial_moves.getValue())
    print("team 0", intermediate_0.getValue())
    print("team 1", intermediate_1.getValue())
    print("team 2", intermediate_2.getValue())
    print("team 3", intermediate_3.getValue())
    print(back_moves.getValue())
else:
    print("No optimal solution found")

# for v in m.getVars():
#     print('%s %g' % (v.VarName, v.X))
# print("obj value is ", m.ObjVal)
