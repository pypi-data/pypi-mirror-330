import random
import math
import numpy as np
from .utils import distance, total_distance

def simulated_annealing(points, initial_temp=10000, cooling_rate=0.995, max_iterations=100000):
    """
    Perform the simulated annealing algorithm to find an approximate solution for TSP.

    Args:
        points (list of tuples): List of (x, y) coordinates.
        initial_temp (float): Initial temperature for simulated annealing.
        cooling_rate (float): Rate at which temperature decreases.
        max_iterations (int): Maximum number of iterations.

    Returns:
        tuple: (best_tour, best_distance)
    """
    num_points = len(points)
    if num_points < 2:
        raise ValueError("At least two points are required to compute a tour.")

    current_tour = list(range(num_points))  # Initial tour (indices)
    random.shuffle(current_tour)  # Random initial order
    current_distance = total_distance(current_tour, points)

    best_tour = current_tour[:]
    best_distance = current_distance

    temperature = initial_temp

    for _ in range(max_iterations):
        i, j = random.sample(range(num_points), 2)  # Pick two points to swap
        new_tour = current_tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]  # Swap points
        new_distance = total_distance(new_tour, points)

        delta = new_distance - current_distance
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_tour = new_tour
            current_distance = new_distance

            if current_distance < best_distance:
                best_tour = current_tour[:]
                best_distance = current_distance

        temperature *= cooling_rate  # Reduce temperature

        if temperature < 1e-10:
            break  # Stop if temperature is too low

    return best_tour, best_distance
