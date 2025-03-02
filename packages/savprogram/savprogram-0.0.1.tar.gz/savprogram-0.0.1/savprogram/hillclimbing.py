# Hill Climbing (Greedy Descent)

def generate_neighbors(x):
    # Generate a list of neighboring solutions
    step_size = 1 # adjust step as needed
    return [x + step_size, x - step_size] # simple neighbors

def hill_climbing(f, x0, max_iterations=1000):
    x = x0 # initial solution
    for _ in range(max_iterations): # prevent infinite loops
        neighbors = generate_neighbors(x) # generate neighbors of x
        # find the neighbor with the highest function value
        best_neighbor = max(neighbors, key=f)
        if f(best_neighbor) <= f(x): # if the best neighbor is not better than x, stop
            return x, f(x)
        x = best_neighbor # otherwise, continue with the best neighbor
    return x, f(x) # return final result
