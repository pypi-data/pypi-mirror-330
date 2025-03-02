import math
import heapq

class Cell:
    """Represents a cell in the grid for A* search."""
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')  # Total cost (g + h)
        self.g = float('inf')  # Cost from start
        self.h = 0  # Heuristic cost

# Define grid size (can be changed dynamically)
ROW = 9
COL = 10

def is_valid(row, col, grid):
    """Check if a cell is within the grid and unblocked."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 1

def is_destination(row, col, dest):
    """Check if a cell is the destination."""
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    """Calculate Euclidean heuristic distance."""
    return math.sqrt((row - dest[0])**2 + (col - dest[1])**2)

def trace_path(cell_details, dest):
    """Trace the path from source to destination."""
    path = []
    row, col = dest
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

    path.append((row, col))
    path.reverse()
    return path

def a_star_search(grid, src, dest):
    """Perform A* search on a given grid."""
    if not is_valid(src[0], src[1], grid) or not is_valid(dest[0], dest[1], grid):
        raise ValueError("Source or destination is invalid or blocked.")

    if is_destination(src[0], src[1], dest):
        return [src]  # Already at destination

    # Initialize cell details
    rows, cols = len(grid), len(grid[0])
    closed_list = [[False for _ in range(cols)] for _ in range(rows)]
    cell_details = [[Cell() for _ in range(cols)] for _ in range(rows)]

    # Initialize the start cell
    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))
    found_dest = False

    # Directions (8 possible moves)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True

        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]

            if is_valid(new_i, new_j, grid) and not closed_list[new_i][new_j]:
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    return trace_path(cell_details, dest)

                g_new = cell_details[i][j].g + 1.0
                h_new = calculate_h_value(new_i, new_j, dest)
                f_new = g_new + h_new

                if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                    heapq.heappush(open_list, (f_new, new_i, new_j))
                    cell_details[new_i][new_j].f = f_new
                    cell_details[new_i][new_j].g = g_new
                    cell_details[new_i][new_j].h = h_new
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j

    raise ValueError("Failed to find a path to the destination.")
