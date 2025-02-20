"""
Calculating Area is easy. Just multiply 4.
Calculating perimeter:

* Check each adjacent (top, left, right, bottom) for a non-matching square OR boundary.
* every non-matching square adds 1 to the perimeter

"""
import numpy as np

def count_diagonals_region(grid: np.array, region: list)->int:
    """
    counts the number of diagonals in a region
    diagonals are two same letters diagonally from each other
    AND there is a same letter either directly above the bottom letter
        OR directly below the top letter
    AND a not same letter either directly above the bottom letter
        OR directly below the top letter
    """

    rows, cols = grid.shape
    pairs = []
    diagonals = 0

    def is_out_of_bounds(row, col):
        return not(0 <= row < rows and 0 <= col < cols)

    # find diagonals
    for location in region:
        target_char =  grid[location[0], location[1]]
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_row, new_col = location[0] + dr, location[1] + dc
            if not is_out_of_bounds(new_row, new_col):
                if grid[new_row, new_col] == target_char:
                    # pairs are always returned with the left most location first
                    if new_col > location[1]:
                        pairs.append([[location[0], location[1]],[new_row, new_col]])
                    else:
                        pairs.append([[new_row, new_col],[location[0], location[1]]])

    unique_pairs_tuples = set(tuple(tuple(inner_list) for inner_list in element) for element in pairs)

    diagonal_pairs = []
    for pair in unique_pairs_tuples:
        """
        qwerk in always arranging left most locaiton first is that diagonals are the same
        """
        left_char = grid[pair[1][0], pair[0][1]]
        right_char = grid[pair[0][0], pair[1][1]]
    
        if (left_char != target_char and right_char == target_char) or \
            (left_char == target_char and right_char != target_char):
            diagonals += 1
            diagonal_pairs.append(pair)
        
   
    # crosses collapse
    # if diagonals form a closed diamond, then the sides reduce by 2 again.
    for pair in diagonal_pairs:
        num = [_ for _ in diagonal_pairs if _[0] == pair[0]]
        if len(num) == 2:
            num = [_ for _ in diagonal_pairs if _[1] == (pair[0][0], pair[0][1]+2)]
            if len(num) == 2:
                if grid[pair[0][0], pair[0][1]+1] != target_char:
                    diagonals -= 1

    print(f"Found {diagonals} diagonals")

    return diagonals


def count_perimeter_cells(grid: np.array, row: int, col: int) -> int:

    rows, cols = grid.shape
    perimeter = 0
    current_val = grid[row, col]

    def is_out_of_bounds(row, col):
        """
        checks for out of bounds. A perimeter must exist if it goes out of bounds
        """
        return not(0 <= row < rows and 0 <= col < cols)

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if is_out_of_bounds(new_row, new_col) or grid[new_row, new_col] != current_val:
            perimeter += 1

    return perimeter

def find_regions(grid, target_char):
    """Finds contiguous regions of a target character in a grid."""

    rows, cols = grid.shape
    visited = set()
    regions = []

    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols

    def dfs(row, col, current_region):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != target_char:
            return

        visited.add((row, col))
        current_region.append((row, col))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Check neighbors
            dfs(row + dr, col + dc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_char and (r, c) not in visited:
                region = []
                dfs(r, c, region)
                if region:  # Add only if the region is not empty
                    regions.append(region)

    return regions



def calculate_price(grid_data: list)->int:

    grid_array = np.array([list(row) for row in grid_data])
    elems = np.unique(grid_array, return_counts=False)
    
    total_price = 0
    for elem in elems:
        regions = find_regions(grid_array, elem)
        for region in regions:
            area = len(region)
            diagonals = count_diagonals_region(grid_array, region)
            sides = 4 + 2 * diagonals
            price = area * sides
            total_price += price
            print(f"The price for {elem} is {area} * {sides} = {price}")

    print(f"The Total price for everything = {total_price}")

    return total_price


def test_sample(file_name:str, answer:int) -> bool:
    with open(file_name, 'r') as f:
        grid_data = [line.strip() for line in f]
    
    if calculate_price(grid_data) == answer:
        return True
    else:
        return False

# assert test_sample('./12/sample0.txt', 80) == True
# assert test_sample('./12/sample2.txt', 436) == True
# assert test_sample('./12/sample3.txt', 236) == True
assert test_sample('./12/sample4.txt', 368) == True

# Part 1

# for elem in elems:
#     perimeter = 0
#     regions = find_regions(grid_array, elem)
#     for region in regions:
#         perimeter = 0
#         area = len(region)
#         for location in region:
#             perimeter += count_perimeter_cells(grid_array, location[0], location[1])
#         price = area * perimeter
#         total_price += price
#         print(f"The price for {elem} is {area} * {perimeter} = {price}")
# print(f"The Total price for everything = {total_price}")

