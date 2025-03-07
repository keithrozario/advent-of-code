
move_deltas = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

def process_file(file_name: str) -> tuple:
    with open(file_name, 'r') as f:
        entire_file = f.readlines()

    warehouse = [line.strip() for line in entire_file if line[0] == '#']
    moves = [line.strip() for line in entire_file if line[0] != '#' and line[0] != '\n']
    moves_str = "".join(moves)
    return warehouse, moves_str


def get_robot_position(warehouse_grid: list) -> list:
    for r, row in enumerate(warehouse_grid):
        try:
            c = row.index('@')
            return [r, c]
        except ValueError:
            pass  # Robot not found in this row, continue searching
    return None

def calc_gps(warehouse_grid: list) -> int:
    gps_sum = 0
    for r,row in enumerate(warehouse_grid):
        for c,col in enumerate(row):
            if col == 'O':
                gps_sum += 100 * r + c
    
    return gps_sum

def solve(warehouse, moves_str):

    warehouse_grid = [list(row) for row in warehouse]
    rows = len(warehouse_grid)
    cols = len(warehouse_grid[0])
    robot_pos = get_robot_position(warehouse_grid)

    moves = list(moves_str)
    # print("Initial state:")
    # for row in warehouse_grid:
    #     print("".join(row))

    for i, move_char in enumerate(moves):
        dr, dc = move_deltas[move_char]
        target_pos = [robot_pos[0] + dr, robot_pos[1] + dc]
        target_cell_content = warehouse_grid[target_pos[0]][target_pos[1]]

        if target_cell_content == '#':
            continue  # Blocked by wall
        
        elif target_cell_content == '.':
            warehouse_grid[robot_pos[0]][robot_pos[1]] = '.'
            warehouse_grid[target_pos[0]][target_pos[1]] = '@'
            robot_pos = target_pos
        
        elif target_cell_content == 'O':
            # Count how many boxes in the direction we're going
            push_pos = [target_pos[0] + dr, target_pos[1] + dc]
            push_cell_content = warehouse_grid[push_pos[0]][push_pos[1]]
            while push_cell_content == 'O':
                push_pos = [push_pos[0] + dr, push_pos[1] + dc]
                push_cell_content = warehouse_grid[push_pos[0]][push_pos[1]]
            
            if not (0 <= push_pos[0] < rows and 0 <= push_pos[1] < cols) or push_cell_content == '#': 
                continue # hits boundary
            elif push_cell_content == '.':
                warehouse_grid[robot_pos[0]][robot_pos[1]] = '.'
                warehouse_grid[target_pos[0]][target_pos[1]] = '@'
                warehouse_grid[push_pos[0]][push_pos[1]] = 'O'
                robot_pos = target_pos

    return warehouse_grid, calc_gps(warehouse_grid)


warehouse, moves_str = process_file('./15/small_sample.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
assert gps == 2028

warehouse, moves_str = process_file('./15/sample.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
assert gps == 10092


warehouse, moves_str = process_file('./15/input.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
print(f"GPS for part 1: {gps}")
