warehouse = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########""".splitlines()
moves_str = "<^^>>>vv<v>>v<<"


warehouse_grid = [list(row) for row in warehouse]
rows = len(warehouse_grid)
cols = len(warehouse_grid[0])

robot_pos = None
for r in range(rows):
    for c in range(cols):
        if warehouse_grid[r][c] == '@':
            robot_pos = [r, c]
            break
    if robot_pos:
        break

moves = list(moves_str)
move_deltas = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }


print("Initial state:")
for row in warehouse_grid:
    print("".join(row))

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
    
    # print(f"Move: {move_char}") # Uncomment to track moves
    # for row in warehouse_grid: # Uncomment to print grid after each move
    #     print("".join(row))
    # print()

gps_sum = 0
for r in range(rows):
    for c in range(cols):
        if warehouse_grid[r][c] == 'O':
            gps_sum += 100 * r + c

print(gps_sum)