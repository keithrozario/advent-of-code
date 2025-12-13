import heapq
import copy
import itertools

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

def add_visit(visited,state,score)->bool:
    """
    visit = set(x,y,direction,score)
    """

    if state not in visited.keys():
        visited[state] = score  
    elif score < visited[state]:
        visited[state] = score
    else:
        pass # visited here before but with a lower score, this is not the best path.

    return visited


def solve_maze(maze):
    grid, start, end = parse_maze(maze)
    visited = dict()
    x,y,direction = start[0], start[1], 'E'
    successful_paths = []

    #  (score, x, y, direction, list of path squares)
    pq = [(0, x, y, 'E', [[x, y]])]
    min_score = 0
    
    while pq:
        score, x, y, direction, path_squares = heapq.heappop(pq)
        
        if (x, y) == end:
            if score <= min_score or min_score == 0:
                min_score = score
                successful_paths.append(path_squares)
        
        # Move forward
        dir_idx = DIR_MAP[direction]
        dx, dy, _ = DIRECTIONS[dir_idx]
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != '#':
                new_score = score+1
                state = (nx, ny, direction,new_score)
                visited = add_visit(visited,state,score)
                if score <= visited[state]:
                    new_path_squares = copy.copy(path_squares)
                    new_path_squares.append([nx,ny])
                    heapq.heappush(pq, (new_score, nx, ny, direction,new_path_squares))
        
        # Rotate clockwise
        new_dir_idx = (dir_idx + 1) % 4
        new_direction = DIRECTIONS[new_dir_idx][2]
        state = (x, y, new_direction)
        new_score = score+1000
        visited = add_visit(visited,state,score)
        if score <= visited[state]:
            heapq.heappush(pq, (new_score, x, y, new_direction,path_squares))
        
        # Rotate counterclockwise
        new_dir_idx = (dir_idx - 1) % 4
        new_direction = DIRECTIONS[new_dir_idx][2]
        state = (x, y, new_direction)
        new_score = score+1000
        visited = add_visit(visited,state,score)
        if score <= visited[state]:
            heapq.heappush(pq, (new_score, x, y, new_direction,path_squares))
        
        # Rotate counterclockwise twice
        new_dir_idx = (new_dir_idx - 1) % 4
        new_direction = DIRECTIONS[new_dir_idx][2]
        state = (x, y, new_direction)
        new_score = score+1000
        visited = add_visit(visited,state,score)
        if score <= visited[state]:
            heapq.heappush(pq, (new_score, x, y, new_direction,path_squares))
    
    return min_score, successful_paths


def count_seats(paths: list)->int:
    all_best_paths = []
    
    # create single list of all squares along the path
    for path in paths:
        all_best_paths.extend(path)

    # de-duplicate
    all_best_paths.sort()
    deduplicate = list(all_best_paths for all_best_paths,_ in itertools.groupby(all_best_paths))

    # return seat count
    return len(deduplicate)


# Tests
with open("./16/sample0.txt", 'r') as f:
    maze = f.read()
score, paths = solve_maze(maze)
assert score == 7036
assert count_seats(paths) == 45

with open("./16/sample.txt", 'r') as f:
    maze = f.read()
score, paths = solve_maze(maze)
assert score == 11048
assert count_seats(paths) == 64

# Part 1 & 2
with open("./16/input.txt", 'r') as f:
    maze = f.read()
score, path = solve_maze(maze)
print(f"Score: {score}")
print(f"Seats: {count_seats(path)}")