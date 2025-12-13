import networkx as nx
import networkx
import heapq
import copy
import itertools

# Directions: (dx, dy, direction)
DIRECTIONS = [(0, 1, 'E'), (1, 0, 'S'), (0, -1, 'W'), (-1, 0, 'N')]
DIR_MAP = {'E': 0, 'S': 1, 'W': 2, 'N': 3}


def file_len(file_name: str)->int:
    with open(file_name) as f:
        lines = f.readlines()

    return len(lines)

def get_line(file_name: str, line_num:int)->int:
    with open(file_name) as f:
        lines = f.readlines()

    return lines[line_num]

def gen_maze(file_name: str, maze_dimension: list[int,int]=[6,6], bytes_fallen: int=12)->list:
    with open(f"{file_name}", 'r') as f:
        blocks = f.readlines()

    block_locations = [ [int(block.strip().split(',')[0]),
                        int(block.strip().split(',')[1])] for block in blocks[:bytes_fallen]]

    grid = []
    for _ in range(maze_dimension[0]+1):
        row = ["."] * (maze_dimension[1]+1)
        grid.append(row)

    for block in block_locations:
        grid[block[1]][block[0]] = "#"

    return grid

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

def solve_maze_networkx(grid, start, end):
    """Solves the maze using networkx."""
    graph = maze_to_graph(grid)
    try:
        path = nx.shortest_path(graph, start, end)
        return len(path) - 1  # Subtract 1 because the path includes start and end
    except nx.NetworkXNoPath:
        return False

# Tests

maze = gen_maze("./18/sample.txt", maze_dimension=[6,6], bytes_fallen=12)
num_steps = solve_maze_networkx(grid=maze, start=(0,0), end=(6,6))
assert num_steps == 22

total_bytes = file_len("./18/sample.txt")
for byte_number in range(13,total_bytes):
    maze = gen_maze("./18/sample.txt", maze_dimension=[6,6], bytes_fallen=byte_number)
    num_steps = solve_maze_networkx(grid=maze, start=(0,0), end=(6,6))
    if not num_steps:
        byte = get_line("./18/sample.txt", byte_number-1)
        break
assert byte.strip() == "6,1"

def find_first_failure_binary(file_name, maze_dimension, low, high):
    """
    Finds the first byte count that causes the maze to be unsolvable using a binary search approach.

    Args:
        file_name: The path to the file containing the maze data.
        maze_dimension: The dimensions of the maze (rows, cols).
        low: The initial lower bound of the search range.
        high: The initial upper bound of the search range.

    Returns:
        The byte number where the maze first becomes unsolvable.
    """
    while low <= high:
        mid = (low + high) // 2
        maze = gen_maze(file_name, maze_dimension=maze_dimension, bytes_fallen=mid)
        if solve_maze_networkx(maze, start=(0, 0), end=maze_dimension):
            low = mid + 1  # Search in the upper half
        else:
            high = mid - 1  # Search in the lower half
    
    return low

# # Part 1
file_name = "./18/input.txt"
maze = gen_maze(file_name=file_name, maze_dimension=(70,70), bytes_fallen=1024)
num_steps = solve_maze_networkx(grid=maze, start=(0,0), end=(70,70))
print(f"Number of steps: {num_steps}")

# # Part 2

# total_bytes = file_len(file_name)
# for byte_number in range(1024,total_bytes):
#     maze = gen_maze(file_name, maze_dimension=[70,70], bytes_fallen=byte_number)
#     if not solve_maze_networkx(grid=maze, start=(0,0), end=(70,70)):
#         byte = get_line(file_name, byte_number-1)
#         break
#     else:
#         print(byte_number)
# print(f"Byte: {byte.strip()}")

first_failure = find_first_failure_binary(file_name=file_name, maze_dimension=(70,70), low=1024, high=file_len(file_name))
byte = get_line(file_name, first_failure-1)
print(f"Byte: {byte.strip()}")