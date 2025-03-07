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




def add_visit(visited,state,num_steps)->bool:
    """
    visit = set(x,y,direction,score)
    """

    if state not in visited.keys():
        visited[state] = num_steps
        visit_status = False  
    elif num_steps < visited[state]:
        visited[state] = num_steps
        visit_status = False
    else:
        visit_status = True

    return visited, visit_status


def solve_maze(grid: list,start: list[int,int]=(0,0), end: tuple[int,int]=(6,6)):
    """
    x is how far from the left
    y is how far from the top
    both start at 0
    """
    visited = {(0,0):0}
    y,x = start[0], start[1]

    #  (score, x, y, list of path squares)
    pq = [(0, y, x, [[y, x]])]
    min_num_steps = 0
    
    while pq:
        num_steps, y, x, path_squares = heapq.heappop(pq)
        
        if (y, x) == end:
            if num_steps <= min_num_steps or min_num_steps == 0:
                min_num_steps = num_steps
            return min_num_steps

       
        # Move forward
        num_steps += 1
        for direction in range(4):
            dx, dy, direction = DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != '#':
                    state = (nx, ny)
                    visited, visit_status = add_visit(visited,state,num_steps)
                    if not visit_status:
                        new_path_squares = copy.copy(path_squares)
                        new_path_squares.append([ny,nx])
                        heapq.heappush(pq, (num_steps, ny, nx, new_path_squares))
    
    return False
 

# Tests

maze = gen_maze("./18/sample.txt", maze_dimension=[6,6], bytes_fallen=12)
num_steps = solve_maze(grid=maze, start=(0,0), end=(6,6))
assert num_steps == 22

total_bytes = file_len("./18/sample.txt")
for byte_number in range(13,total_bytes):
    maze = gen_maze("./18/sample.txt", maze_dimension=[6,6], bytes_fallen=byte_number)
    num_steps = solve_maze(grid=maze, start=(0,0), end=(6,6))
    if not num_steps:
        byte = get_line("./18/sample.txt", byte_number-1)
        break
assert byte.strip() == "6,1"



# # Part 1
file_name = "./18/input.txt"
maze = gen_maze(file_name=file_name, maze_dimension=(70,70), bytes_fallen=1024)
num_steps = solve_maze(grid=maze, start=(0,0), end=(70,70))
print(f"Number of steps: {num_steps}")

# # Part 2

total_bytes = file_len(file_name)
for byte_number in range(1024,total_bytes):
    maze = gen_maze(file_name, maze_dimension=[70,70], bytes_fallen=byte_number)
    if not solve_maze(grid=maze, start=(0,0), end=(70,70)):
        byte = get_line(file_name, byte_number-1)
        break
    else:
        print(byte_number)
print(f"Byte: {byte.strip()}")