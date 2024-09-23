import numpy as np

def generate_initial_tour(n, home):
    # Create an initial tour with alternating home and away games to respect constraints
    tour = [home]  # Start with a home game
    for i in range(2, n + 1):
        if i != home:
            tour.append(i)
        tour.append(home)
    
    return tour[:n + n - 1]  # Ensure the tour is of length 2n-1

def optimize_tour(tour, distance_matrix, l, u, home):
    n = len(tour)
    # Attempt to swap to minimize distance while respecting constraints
    best_tour = tour[:]
    min_distance = calculate_tour_distance(tour, distance_matrix)
    
    # Simple optimization: try swapping two locations and check improvement
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if tour[i] != home and tour[j] != home:  # Ensure we don't swap home games
                tour[i], tour[j] = tour[j], tour[i]
                if is_valid_tour(tour, l, u, home) and calculate_tour_distance(tour, distance_matrix) < min_distance:
                    min_distance = calculate_tour_distance(tour, distance_matrix)
                    best_tour = tour[:]
                tour[i], tour[j] = tour[j], tour[i]  # Swap back
    
    return best_tour, min_distance

def calculate_tour_distance(tour, distance_matrix):
    distance = 0
    for i in range(1, len(tour)):
        distance += distance_matrix[tour[i-1]-1][tour[i]-1]
    return distance

def is_valid_tour(tour, l, u, home):
    # Check if the tour meets the constraints of l and u for home stands and road trips
    current_place = tour[0]
    count = 0
    for place in tour:
        if place == current_place:
            count += 1
        else:
            if current_place == home and not(l <= count <= u):
                return False
            if current_place != home and not(l <= count <= u):
                return False
            current_place = place
            count = 1
    # Final check for the last sequence of games
    if (current_place == home and not(l <= count <= u)) or (current_place != home and not(l <= count <= u)):
        return False
    return True

# Example usage
n = 6
home_team = 1
l, u = 1, 3  # Constraints on the length of home stands and road trips
distance_matrix = np.array([
    [0, 29, 20, 21, 30, 40],
    [29, 0, 15, 17, 25, 35],
    [20, 15, 0, 28, 22, 37],
    [21, 17, 28, 0, 19, 31],
    [30, 25, 22, 19, 0, 12],
    [40, 35, 37, 31, 12, 0]
])

# distance_matrix = [[1 for _ in range(10)] for _ in range(n)]

initial_tour = generate_initial_tour(n, home_team)
optimized_tour, min_distance = optimize_tour(initial_tour, distance_matrix, l, u, home_team)
print("Optimized Tour:", optimized_tour)
print("Minimum Distance:", min_distance)
