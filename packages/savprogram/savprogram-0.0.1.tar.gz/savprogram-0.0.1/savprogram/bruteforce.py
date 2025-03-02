# Brute Force
import itertools
import time
import numpy as np
from .utils import distance, total_distance

def tsp_brute_force(points):
    """
    Find the optimal TSP route using brute force.

    Args:
        points (list of tuples): List of (x, y) coordinates representing locations.

    Returns:
        tuple: (best_route, min_distance, execution_time)
    """
    num_points = len(points)
    all_indices = range(num_points)
    min_distance = float('inf')
    best_route = None

    start_time = time.time()
    for perm in itertools.permutations(all_indices):
        current_distance = total_distance(perm, points)
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = perm
    execution_time = time.time() - start_time

    return best_route, min_distance, execution_time
