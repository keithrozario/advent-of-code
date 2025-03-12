
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

def check_obstruction(full_box_pos: list, warehouse_grid: list, move_char: str) -> bool:
    """
    checks if there is an obstruction in the path of the box
    """
    dr, dc = move_deltas[move_char]
    if warehouse_grid[full_box_pos[0][0]+dr][full_box_pos[0][1] + dc] == '#' or \
    warehouse_grid[full_box_pos[1][0]+dr][full_box_pos[1][1] + dc] == '#':
        return True
    return False

def remove_duplicates_boxes_and_order(boxes: list, move_char: str) -> list:
    """
    Removes duplicate boxes from a list while preserving order.
    Args:
        boxes: The list potentially containing duplicates.
    Returns:
        A new list with duplicates removed, maintaining the original order.
    """
    seen = set()
    result = []
    for box in boxes:
        box_left = tuple(box[0])
        if box_left not in seen:
            seen.add(box_left)
            result.append(box)
    
    if move_char == 'v':
        boxes_in_order = list(reversed(sorted(result, key=lambda inner_list: inner_list[0][0])))
    elif move_char == '^':
        boxes_in_order = list(sorted(result, key=lambda inner_list: inner_list[0][0]))
    else:
        raise("Invalid move_char")
            
    return boxes_in_order


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
            if col == 'O' or col == '[': # since we measure from the top left edge, closes edge of box is always the '['
                gps_sum += 100 * r + c
    
    return gps_sum

def get_full_box_pos(box_pos: list, warehouse_grid: list) -> list:
    """
    returns the two positions of the box in a list
    """

    if warehouse_grid[box_pos[0]][box_pos[1]] == '[':
    # full_box_pos has the two locations of both sides of the box
        full_box_pos = [box_pos, [box_pos[0], box_pos[1]+1]]
    else:
        full_box_pos = [[box_pos[0], box_pos[1]-1], box_pos]

    return full_box_pos

def move_box_up_down(full_box_pos: list, warehouse_grid: list, move_char: str) -> list:
    """
    moves a box up or down
    """
    dr, dc = move_deltas[move_char]

    # Only move the box if the new position is empty for both sides
    if warehouse_grid[full_box_pos[0][0]+dr][full_box_pos[0][1] + dc] == '.' and \
    warehouse_grid[full_box_pos[1][0]+dr][full_box_pos[1][1] + dc] == '.':
        warehouse_grid[full_box_pos[0][0]][full_box_pos[0][1]] = '.'
        warehouse_grid[full_box_pos[1][0]][full_box_pos[1][1]] = '.'
        warehouse_grid[full_box_pos[0][0]+dr][full_box_pos[0][1] + dc] = '['
        warehouse_grid[full_box_pos[1][0]+dr][full_box_pos[1][1] + dc] = ']'

    return warehouse_grid

def get_boxes_vertical(warehouse_grid: list, vertical_boxes: list, move_char: str) -> list:
    """
    Args:
        warehouse_grid: warehouse grid

        vertical_boxes: list of box positions
    Returns:
        a list of box positions for boxes that are in the direction of move_char from very box in vertical_boxes
    """
    vertical_box_positions = []
    dr,dc = move_deltas[move_char]
    for full_box_pos in vertical_boxes:
        if warehouse_grid[full_box_pos[0][0]+dr][full_box_pos[0][1] + dc] in ['[',']']:
            vertical_box_positions.append(get_full_box_pos([full_box_pos[0][0]+dr, full_box_pos[0][1] + dc], warehouse_grid))
        if warehouse_grid[full_box_pos[1][0]+dr][full_box_pos[1][1] + dc] in ['[',']']:
            vertical_box_positions.append(get_full_box_pos([full_box_pos[1][0]+dr, full_box_pos[1][1] + dc], warehouse_grid))
    return vertical_box_positions


def solve_new(warehouse, moves_str):

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
        
        elif target_cell_content == '[' or target_cell_content == ']':
            """
            e.g. if moving one step >.

                    push_pos (where the boxes will end up)
                      v
            ...@[][][]...
                ^
             target_pos (where the robot will end up)
            """
            # Count how many boxes in the direction we're going
            push_pos = [target_pos[0] + dr, target_pos[1] + dc]
            push_cell_content = warehouse_grid[push_pos[0]][push_pos[1]]
            while push_cell_content == '[' or push_cell_content == ']':
                push_pos = [push_pos[0] + dr, push_pos[1] + dc]
                push_cell_content = warehouse_grid[push_pos[0]][push_pos[1]]
            
            if not (0 <= push_pos[0] < rows and 0 <= push_pos[1] < cols) or push_cell_content == '#': 
                continue # hits boundary
            elif push_cell_content == '.':

                if move_char == '<' or move_char == '>':
                    # Start from the end of the boxes
                    box_pos = [push_pos[0] - dr, push_pos[1] - dc]
                    box_cell_content = warehouse_grid[box_pos[0]][box_pos[1]]
                    while box_cell_content == '[' or box_cell_content == ']':
                        warehouse_grid[box_pos[0]+dr][box_pos[1] + dc] = box_cell_content
                        box_pos = [box_pos[0] - dr, box_pos[1] - dc]
                        box_cell_content = warehouse_grid[box_pos[0]][box_pos[1]]
                    
                    warehouse_grid[robot_pos[0]][robot_pos[1]] = '.'
                    warehouse_grid[target_pos[0]][target_pos[1]] = '@'
                    robot_pos = target_pos
                else:
                    """
                    e.g. if moving one step ^.

                            ...
                            ...
                            .[]
           full_box_pos[0] >[]< full_box_pos[1]
                            @< robot_pos
                            ...
                            ...
                    boxes_to_move = [ [full_box_pos[0],full_box_pos[1]],  [[x1,y1],[x1,y2]] ]
                    
                    * full_box_pos[0] is a list of the x,y coordinates of the left side of the box
                    * full_box_pos[1] is a list of the x,y coordinates of the right side of the box
                    """
                    ### get full list of boxes to move
                    full_box_pos = get_full_box_pos(target_pos, warehouse_grid)
                    boxes_in_the_way = []
                    vertical_boxes = [full_box_pos]
                    while len(vertical_boxes)>0:
                        boxes_in_the_way.extend(vertical_boxes)
                        vertical_boxes = get_boxes_vertical(warehouse_grid, vertical_boxes, move_char)
                    boxes_to_move = remove_duplicates_boxes_and_order(boxes_in_the_way, move_char)
                    
                    # Check if any of the boxes to move are obstructed, if even one is obstructed, nothing moves.
                    if any(check_obstruction(full_box_pos, warehouse_grid, move_char) for full_box_pos in boxes_to_move):
                        continue

                    # iterate through the list (it's already ordered in the direction of moving), move boxes
                    for full_box_pos in boxes_to_move:
                        warehouse_grid = move_box_up_down(full_box_pos, warehouse_grid, move_char)
                    # move robot
                    warehouse_grid[robot_pos[0]][robot_pos[1]] = '.'
                    warehouse_grid[target_pos[0]][target_pos[1]] = '@'
                    robot_pos = target_pos
                       
    return warehouse_grid, calc_gps(warehouse_grid)


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


def modify_warehouse(warehouse_grid: list) -> list:
    new_warehouse = []
    for row in warehouse_grid:
        new_row = []
        for col in row:
            if col == 'O':
                new_row.append('[')
                new_row.append(']')
            elif col == '.':
                new_row.append('.')
                new_row.append('.')
            elif col == '#':
                new_row.append('#')
                new_row.append('#')
            elif col == '@':
                new_row.append('@')
                new_row.append('.')
        new_warehouse.append(new_row)

    return new_warehouse


warehouse, moves_str = process_file('./15/small_sample.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
assert gps == 2028

warehouse, moves_str = process_file('./15/sample.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
assert gps == 10092


warehouse, moves_str = process_file('./15/input.txt')
warehouse_grid, gps = solve(warehouse, moves_str)
print(f"GPS for part 1: {gps}")
assert gps == 1526673


warehouse, moves_str = process_file('./15/sample.txt')
new_warehouse = modify_warehouse(warehouse)
solution, gps = solve_new(new_warehouse, moves_str)
assert gps == 9021


warehouse, moves_str = process_file('./15/reddit_2.txt')
new_warehouse = modify_warehouse(warehouse)
solution, gps = solve_new(new_warehouse, moves_str)
assert gps == 1216

warehouse, moves_str = process_file('./15/input.txt')
new_warehouse = modify_warehouse(warehouse)
solution, gps = solve_new(new_warehouse, moves_str)
print(f"GPS for part 2: {gps}")