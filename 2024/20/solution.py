import networkx
import numpy as np
import copy


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
        graph.remove_edge((ny, nx), (y, x))  # remove edge to neighbor
    return graph

def solve_maze_networkx(grid, start, end):
    """Solves the maze using networkx."""
    graph = maze_to_graph(grid)
    try:
        path = networkx.shortest_path(graph, start, end)
        return len(path) - 1, path  # Subtract 1 because the path includes start and end
    except networkx.NetworkXNoPath:
        return False


def solve_maze_networkx_from_graph(graph, start, end):
    try:
        path = networkx.shortest_path(graph, start, end)
        return len(path) - 1, path  # Subtract 1 because the path includes start and end
    except networkx.NetworkXNoPath:
        return False


def find_wall_coordinates(grid, target_char: str="#"):
    np_grid = np.array([list(row) for row in grid])
    coordinates = np.argwhere(np_grid == target_char)
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


def check_cheats(grid, graph, base_picoseconds,path,min_time_saved: int=10):
    cheats = {}

    wall_locations = find_wall_coordinates(grid)
    for cheat_index, location in enumerate(wall_locations):
        graph = add_wall_to_graph(graph, location)
        new_picoseconds,_ = solve_maze_networkx_from_graph(graph, start, end)
        if new_picoseconds < base_picoseconds:
            time_saved = base_picoseconds-new_picoseconds
            if time_saved >= min_time_saved:
                cheats[time_saved] = cheats.get(time_saved,0)+1

        graph = remove_wall_to_graph(graph, location)
        print(f"{cheat_index} of {len(wall_locations)}")
    sorted_cheats = dict(sorted(cheats.items()))

    return sorted_cheats


# Test
with open("./20/sample.txt", 'r') as f:
    maze = f.read()
grid, start, end = parse_maze(maze)
graph = maze_to_graph(grid)

base_picoseconds, path = solve_maze_networkx_from_graph(graph, start, end)
assert base_picoseconds == 84
cheats = check_cheats(grid, graph, base_picoseconds, path, min_time_saved=0)
assert cheats[2] == 14
cheats = check_cheats(grid, graph, base_picoseconds, path, min_time_saved=63)
total_cheats = 0
for cheat in cheats.keys():
    total_cheats += cheats[cheat]
assert total_cheats == 1


# Part 1
with open("./20/input.txt", 'r') as f:
    maze = f.read()
grid, start, end = parse_maze(maze)
graph = maze_to_graph(grid)
base_picoseconds, path = solve_maze_networkx_from_graph(graph, start, end)
print("solve")
cheats = check_cheats(grid, graph, base_picoseconds, path, min_time_saved=100)
total_cheats = 0
for cheat in cheats.keys():
    total_cheats += cheats[cheat]
print(f"Total Cheats saving at least 100 picoseconds: {total_cheats}")