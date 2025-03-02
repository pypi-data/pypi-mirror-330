import numpy as np

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(route, points):
    """Compute the total distance of the given route."""
    return sum(distance(points[route[i]], points[route[i+1]]) for i in range(len(route)-1)) + distance(points[route[-1]], points[route[0]])
