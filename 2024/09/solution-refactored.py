"""
Doesn't work at all!!! :(

"""


from collections import Counter
from itertools import groupby

def find_free_space(physical_map, num_blocks):
    """Finds the index of the first free space of at least num_blocks."""
    for i, char in enumerate(physical_map):
        if char == '.':
            count = 0
            for j in range(i, len(physical_map)):
                if physical_map[j] == '.':
                    count += 1
                else:
                    break
                if count >= num_blocks: return i
    return -1

def gen_physical_map(disk_map: str):
    """Generates the physical map from the disk map string."""
    physical_map = []
    for i, num_str in enumerate(disk_map):
        num = int(num_str)
        if i % 2 == 0:
            physical_map.extend([str(i // 2)] * num)
        else:
            physical_map.extend(['.'] * num)
    return physical_map

def defragment(physical_map):
    """Defragments the physical map by moving files to the left."""
    next_free = 0
    for i in range(len(physical_map)):
        if physical_map[i] != '.':
            if i != next_free:
                physical_map[next_free], physical_map[i] = physical_map[i], physical_map[next_free]
            next_free += 1
    return physical_map

def calculate_checksum(physical_map):
    """Calculates the checksum of the defragmented map."""
    checksum = 0
    for i, block in enumerate(physical_map):
        if block != '.':
            checksum += i * int(block)
    return checksum

# --- Main execution ---

def solve_part1(disk_map):
    physical_map = gen_physical_map(disk_map)
    physical_map = defragment(physical_map)
    return calculate_checksum(physical_map)


def solve_part2(disk_map):
    physical_map = gen_physical_map(disk_map)
    file_sizes = Counter(physical_map)
    
    for file_id in range(len(file_sizes) -1, 0,-1):
        file_size = file_sizes[str(file_id)]
        first_free = find_free_space(physical_map, file_size)
        if first_free == -1:  # Handle cases where file is already correctly positioned 
            continue # move to next file
        current_pos = physical_map.index(str(file_id))
        if first_free < current_pos:
            for _ in range(file_size):
                current_pos = physical_map.index(str(file_id))  # Recalculate as it can move
                physical_map[first_free], physical_map[current_pos] = physical_map[current_pos], physical_map[first_free]
                first_free += 1

    return calculate_checksum(physical_map)


with open("./09/input.txt", "r") as input_file:
    disk_map = input_file.read().strip()

checksum1 = solve_part1(disk_map)
print(f"Checksum for part 1: {checksum1}")

checksum2 = solve_part2(disk_map)
print(f"Checksum for part 2: {checksum2}")

