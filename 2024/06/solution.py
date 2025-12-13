import numpy as np

arrows = ['>','<','^','v']

def get_guard_location(map: np.array) -> tuple:
    """
    returns (tuple):
        tuple: the location of the arrow in the map in (x,y) tuple
        direction: arrow direction ('>','<','^','v')
    """
    for arrow in arrows:
        try:
            arrow_location = np.where(map == arrow)
            return {
                "direction": arrow,
                "location": [int(arrow_location[0][0]), int(arrow_location[1][0])]
                }
        except IndexError:
            print("Guard Not found, must be end of the map\n\n")
    


def going_out_of_map(y: int, x:int, max_y: int, max_x: int, arrow)->bool:
    """
    Returns True if the next step is out of bounds
    """
    if arrow == '^' and y == 0:
        return True
    if arrow == '<' and x == 0:
        return True
    if arrow == '>' and x == max_x:
        return True
    if arrow == 'v' and y == max_y:
        return True
    
    return False


def move_one_step(guard_map: np.array, guard_location: dict):
    """
    Moves the guard up until it hits an obstacle.
    """

    y = guard_location['location'][0]
    x = guard_location['location'][1]
    arrow = guard_location['direction']
    reached_end_of_map = False

    # numpy like python allows negative indices (wrap-around)
    # we cannot rely on IndexErrors to catch going out of bounds
    if going_out_of_map(y=y, x=x, max_y=len(guard_map)-1, max_x=len(guard_map[0])-1, arrow=arrow):
        guard_map[y,x] = 'X'
        reached_end_of_map = True
    else:
        if arrow == '^':
            next_step = guard_map[y-1, x]
            if next_step == '#':
                guard_map[y, x] = '>'
            else:
                guard_map[y, x] = 'X'
                guard_map[y-1, x] = arrow
                guard_location['location'][0] = y-1
        elif arrow == '>':
            next_step = guard_map[y, x+1]
            if next_step == '#':
                guard_map[y, x] = 'v'
            else:
                guard_map[y, x] = 'X'
                guard_map[y, x+1] = arrow
                guard_location['location'][1] = x+1
        elif arrow == 'v':
            next_step = guard_map[y+1, x]
            if next_step == '#':
                guard_map[y, x] = '<'
            else:
                guard_map[y, x] = 'X'
                guard_map[y+1, x] = arrow
                guard_location['location'][0] = y+1
        elif arrow == '<':
            next_step = guard_map[y, x-1]
            if next_step == '#':
                guard_map[y, x] = '^'
            else:
                guard_map[y, x] = 'X'
                guard_map[y, x-1] = arrow
                guard_location['location'][1] = x-1
        
        guard_location['direction'] = guard_map[guard_location['location'][0], guard_location['location'][1]]
    
    return guard_map, reached_end_of_map, guard_location

def move_one_step_get_barriers(guard_map: np.array, guard_location: dict):
    """
    Moves the guard one step based on the arrow direction.
    Returns location of obstacles as well.
    """

    y = guard_location['location'][0]
    x = guard_location['location'][1]
    arrow = guard_location['direction']
    reached_end_of_map = False
    obstacle_location = None

    # numpy like python allows negative indices (wrap-around)
    # we cannot rely on IndexErrors to catch going out of bounds
    if going_out_of_map(y=y, x=x, max_y=len(guard_map)-1, max_x=len(guard_map[0])-1, arrow=arrow):
        guard_map[y,x] = 'X'
        reached_end_of_map = True
    else:
        if arrow == '^':
            next_step = guard_map[y-1, x]
            if next_step == '#':
                obstacle_location = [y-1, x]
                guard_map[y, x] = '>'
            else:
                guard_map[y, x] = 'X'
                guard_map[y-1, x] = arrow
                guard_location['location'][0] = y-1
        elif arrow == '>':
            next_step = guard_map[y, x+1]
            if next_step == '#':
                obstacle_location = [y, x+1]
                guard_map[y, x] = 'v'
            else:
                guard_map[y, x] = 'X'
                guard_map[y, x+1] = arrow
                guard_location['location'][1] = x+1
        elif arrow == 'v':
            next_step = guard_map[y+1, x]
            if next_step == '#':
                guard_map[y, x] = '<'
                obstacle_location = [y+1, x]
            else:
                guard_map[y, x] = 'X'
                guard_map[y+1, x] = arrow
                guard_location['location'][0] = y+1
        elif arrow == '<':
            next_step = guard_map[y, x-1]
            if next_step == '#':
                guard_map[y, x] = '^'
                obstacle_location = [y, x-1]
            else:
                guard_map[y, x] = 'X'
                guard_map[y, x-1] = arrow
                guard_location['location'][1] = x-1
        
        guard_location['direction'] = guard_map[guard_location['location'][0], guard_location['location'][1]]
    
    return guard_map, reached_end_of_map, guard_location, obstacle_location
    
# Question 1

# # Get input
# with open('./06/input.txt', 'r') as input:
#     lines = input.readlines()
#     guard_map = np.array([list(line.strip()) for line in lines])

# reached_end_of_map = False
# # find guard
# guard_location = get_guard_location(guard_map)

# while not reached_end_of_map:
#     guard_map, reached_end_of_map, guard_location = move_one_step(guard_map, guard_location)

# num_x = np.count_nonzero(guard_map == 'X')
# print(f"Nuber of 'X's is {num_x}")

# Question 2

# Get input
with open('./06/input.txt', 'r') as input:
    lines = input.readlines()
    guard_map = np.array([list(line.strip()) for line in lines])

reached_end_of_map = False
# find guard
guard_location = get_guard_location(guard_map)
obstacle_locations = []

while not reached_end_of_map:
    guard_map, reached_end_of_map, guard_location, obstacle_location = move_one_step_get_barriers(guard_map, guard_location)
    if obstacle_location: obstacle_locations.append(obstacle_location)

num_x = np.count_nonzero(guard_map == 'X')
print(f"Nuber of 'X's is {num_x}")
print(obstacle_locations)

"""
Part 2 doesn't work :(
"""