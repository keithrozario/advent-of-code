import numpy as np
import itertools

def parse_file(file_name: str)->tuple[np.ndarray, tuple]:
    
    with open(file_name, 'r') as file:
        grid = np.array([list(line.strip()) for line in file])

    unique_chars = set(grid.flatten()) - {'.'}
    
    character_coords = {}
    for char in unique_chars:
        character_coords[char]=find_coordinates(grid,char)
    
    return grid, character_coords

def find_coordinates(grid, char):
    coordinates = np.argwhere(grid == char)
    return [tuple(coord) for coord in coordinates]

def check_bounds(point: tuple[int,int], height, width)->bool:
    
    if 0<= point[0] < width and 0 <= point[1] < height:
        return True
    
    return False

def get_pair_antinodes(a1: tuple[int,int], a2: tuple[int,int], height: int, width: int):
    
    antinodes = []

    dx = a1[0]-a2[0]
    dy = a1[1]-a2[1]
    a3 = (a1[0] + dx, a1[1]+dy)
    a4 = (a2[0] - dx, a2[1]-dy)

    for point in (a3,a4):
        if check_bounds(point, height, width):
            antinodes.append(point)
    
    return antinodes

def get_pair_antinodes_part_2(a1: tuple[int,int], a2: tuple[int,int], height: int, width: int):
    
    antinodes = []

    dx = a1[0]-a2[0]
    dy = a1[1]-a2[1]

    # go positive direction +dx +dy
    point = a1
    while True:
        point = (point[0] + dx, point[1] + dy)
        if check_bounds(point, height, width):
            antinodes.append(point)
        else:
            break
    
    # go negative direction -dx -dy
    point = a2
    while True:
        point = (point[0] - dx, point[1] - dy)
        if check_bounds(point, height, width):
            antinodes.append(point)
        else:
            break
    
    return antinodes

def find_antinodes(character_coords: dict, height: int, width: int):
    antinodes = []
    antinodes_part_2 = []
    for char in character_coords:
        locations = character_coords[char]
        pairs = list(itertools.combinations(locations, 2))
        for pair in pairs:
            antinodes.extend(get_pair_antinodes(pair[0], pair[1], height, width))

            # Part 2
            part_2_antinodes = get_pair_antinodes_part_2(pair[0], pair[1], height, width)
            antinodes_part_2.extend(part_2_antinodes)
            antinodes_part_2.extend(pair)

    # de-duplicate
    de_duplicate_antinodes = set(antinodes)
    de_duplicate_antinodes_part_2 = set(antinodes_part_2)

    return de_duplicate_antinodes, de_duplicate_antinodes_part_2

# Tests
grid, character_coords = parse_file("./08/sample.txt")
antinodes, antinodes_part_2 = find_antinodes(character_coords=character_coords, height=grid.shape[0], width=grid.shape[1] )
assert len(antinodes) == 14
assert len(antinodes_part_2) == 34

# Part 1
grid, character_coords = parse_file("./08/input.txt")
antinodes, antinodes_part_2 = find_antinodes(character_coords=character_coords, height=grid.shape[0], width=grid.shape[1] )
print(f"Number of antinodes: {len(antinodes)}")
print(f"Number of antinodes in part 2: {len(antinodes_part_2)}")