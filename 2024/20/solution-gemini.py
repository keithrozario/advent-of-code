import networkx
import numpy as np
import copy
from collections import deque

# Directions: (dx, dy, direction)
DIRECTIONS = [(0, 1, 'E'), (1, 0, 'S'), (0, -1, 'W'), (-1, 0, 'N')]
DIR_MAP = {'E': 0, 'S': 1, 'W': 2, 'N': 3}

def parse_maze(maze):
    start = end = None
    grid = []
    for r, line in enumerate(maze.strip().split('\n')):
        grid.append(line)
        if 'S' in line:
            start = (r, line.index('S'))
        if 'E' in line:
            end = (r, line.index('E'))
    return grid, start, end

def maze_to_graph(grid):
    """Converts the maze grid to a networkx graph."""
    graph = networkx.Graph()
    rows = len(grid)
    cols = len(grid[0])

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != '#':  # Add node if not a wall
                # Add edges to valid neighbors
                for dx, dy, _ in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != '#':
                        graph.add_edge((y, x), (ny, nx))  # Add edge to neighbor
    return graph

def add_wall_to_graph(graph, wall_location):
    y,x = wall_location
    
    for dx, dy, _ in DIRECTIONS:
        nx, ny = x + dx, y + dy
        graph.add_edge((ny, nx), (y, x))  # Add edge to neighbor
    
    return graph

def remove_wall_to_graph(graph, wall_location):
    y,x = wall_location
    for dx, dy, _ in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if graph.has_edge((ny,nx),(y,x)):
            graph.remove_edge((ny, nx), (y, x))  # remove edge to neighbor
    return graph

def solve_maze_networkx(grid, start, end):
    """Solves the maze using networkx."""
    graph = maze_to_graph(grid)
    try:
        path = networkx.shortest_path(graph, start, end)
        return len(path) - 1, path  # Subtract 1 because the path includes start and end
    except networkx.NetworkXNoPath:
        return False, []
    
def solve_maze_networkx_from_graph(graph, start, end):
    try:
        path = networkx.shortest_path(graph, start, end)
        return len(path) - 1, path  # Subtract 1 because the path includes start and end
    except networkx.NetworkXNoPath:
        return False, []


def find_wall_coordinates(grid, target_char: str="#"):
    """
    Finds the coordinates of all elements in a 2D array (grid) that are equal to a target character.

    Args:
        grid: A list of strings representing the 2D array.
        target_char: The character to search for.

    Returns:
        A list of tuples, where each tuple represents the (row, column) coordinates of an element
        equal to the target character.
    """

    # Convert the list of strings to a NumPy array of characters
    np_grid = np.array([list(row) for row in grid])

    # Use np.argwhere to find the indices where the array equals the target character
    coordinates = np.argwhere(np_grid == target_char)

    # Convert the NumPy array of coordinates to a list of tuples
    return [(row, col) for row, col in coordinates]

def check_wall_on_path(wall: list[int,int], path: list[tuple[int,int]])->bool:

    if wall[0]==0 or wall[1]==0:
        return False
    else:
        y,x = wall
        for dx, dy, _ in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if (ny,nx) in path:
                return True

    return False

def is_valid(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def get_neighbors(r, c, grid):
    neighbors = []
    for dr, dc, _ in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if is_valid(nr, nc, grid):
            neighbors.append((nr, nc))
    return neighbors

def find_cheats(grid, graph, base_picoseconds, path, min_time_saved=100, max_cheat_length=20):
    cheats = {}
    wall_locations = [wall for wall in find_wall_coordinates(grid) if check_wall_on_path(wall, path)]
    for start_wall in wall_locations:
        for cheat_length in range(1, max_cheat_length + 1):
            
            q = deque([(start_wall, 0, [start_wall])])
            visited = set()

            while q:
                current_wall, current_cheat_length, cheat_path = q.popleft()

                if (current_wall, current_cheat_length) in visited:
                    continue
                visited.add((current_wall, current_cheat_length))

                
                if current_cheat_length == cheat_length:
                    
                    if check_wall_on_path(current_wall, path):
                        temp_graph = copy.deepcopy(graph)

                        for node in cheat_path:
                            temp_graph = remove_wall_to_graph(temp_graph, node)

                        new_picoseconds, _ = solve_maze_networkx_from_graph(temp_graph, start, end)

                        if new_picoseconds != False and new_picoseconds < base_picoseconds:
                            time_saved = base_picoseconds - new_picoseconds
                            if time_saved >= min_time_saved:
                                cheats[(tuple(start_wall),tuple(current_wall))] = cheats.get((tuple(start_wall),tuple(current_wall)), 0) + 1
                    continue

                for neighbor in get_neighbors(current_wall[0], current_wall[1], grid):
                   if grid[neighbor[0]][neighbor[1]] == "#":
                        new_cheat_path = copy.copy(cheat_path)
                        new_cheat_path.append(neighbor)
                        q.append((neighbor, current_cheat_length+1, new_cheat_path))

    return cheats

# Test
with open("./20/sample.txt", 'r') as f:
    maze = f.read()
grid, start, end = parse_maze(maze)
graph = maze_to_graph(grid)
base_picoseconds, path = solve_maze_networkx_from_graph(graph, start, end)
assert base_picoseconds == 84

cheats = find_cheats(grid, graph, base_picoseconds, path, min_time_saved=0, max_cheat_length=2)
assert cheats.get(((1, 8), (1, 9)), 0) == 1

cheats = find_cheats(grid, graph, base_picoseconds, path, min_time_saved=50, max_cheat_length=6)
assert cheats.get(((1, 8), (0, 8)), 0) == 1
assert cheats.get(((4, 2), (5, 2)), 0) == 1

cheats = find_cheats(grid, graph, base_picoseconds, path, min_time_saved=0, max_cheat_length=20)
total_cheats = 0
for cheat in cheats.keys():
    total_cheats += cheats[cheat]
assert total_cheats == 42


# Part 1
with open("./20/input.txt", 'r') as f:
    maze = f.read()
grid, start, end = parse_maze(maze)
graph = maze_to_graph(grid)
base_picoseconds, path = solve_maze_networkx_from_graph(graph, start, end)
cheats = find_cheats(grid, graph, base_picoseconds, path, min_time_saved=100, max_cheat_length=2)
total_cheats = 0
for cheat in cheats.keys():
    total_cheats += cheats[cheat]
print(f"Total Cheats saving at least 100 picoseconds: {total_cheats}")

# Part 2
cheats = find_cheats(grid, graph, base_picoseconds, path, min_time_saved=100, max_cheat_length=20)
total_cheats = 0
for cheat in cheats.keys():
    total_cheats += cheats[cheat]
print(f"Total Cheats saving at least 100 picoseconds: {total_cheats}")
