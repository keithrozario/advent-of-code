from collections import Counter

from itertools import groupby

def find_free_space(physical_map, num_blocks):
    """Finds the index of the first occurrence of n consecutive dots using groupby.

    Args:
        data: The list of characters.
        n: The number of consecutive dots to search for.

    Returns:
        The index of the first dot in the sequence, or -1 if not found.
    """
    index = 0
    for key, group in groupby(physical_map):
        length = len(list(group))
        if key == "." and length >= num_blocks:
            return index
        index += length
    return -1

def gen_physical_map(disk_map: str):
    """
    returns a list of the physical representation, where every block corresponds to one element on the list
    a free space is represented by a '.' in the element location
    a file is represented by the the FILE_ID in the element location    
    """
    
    physical_map = []
    for i, num in enumerate(disk_map):
        num = int(num)
        if i % 2 == 0: # file
            for _ in range(num):
                physical_map.append(str(int(i/2)))
        else: # free space
            physical_map.extend('.' * num)
    
    return physical_map



def find_first_free_block(physical_map):
    first_free = physical_map.index('.')

    for i in range(len(physical_map)-1, -1, -1):
        if physical_map[i] != '.':
            last_file_location = i
            break

    return first_free, last_file_location

def find_last_file(physical_map, processed_file_ids):
    """
    Args:
        physical_map: the map of the current list
        processed_file_ids: list of file ids that have already been processed
    returns:
        the location and id of the last file
        ignores any files already processed in 'processed_file_ids'
    """

    for i in range(len(physical_map)-1, -1, -1):
        if physical_map[i] != '.':
            if physical_map[i] not in processed_file_ids:
                last_file_location = i
                last_file_id = physical_map[i]
                break

    return last_file_location, last_file_id

def swap_positions(last_file, first_free, physical_map):
    """
    swap positions of last_file and first_free in list
    """
    temp = physical_map[last_file]
    physical_map[last_file] = physical_map[first_free]
    physical_map[first_free] = temp
    return physical_map

## Read in input txt
with open("./09/input.txt", "r") as input:
    disk_map = input.read().strip()
physical_map = gen_physical_map(disk_map=disk_map)

# Re-arrange
while True:
    first_free, last_file_location = find_first_free_block(physical_map)
    if first_free > last_file_location:
        break
    else:
        physical_map = swap_positions(last_file_location, first_free, physical_map)

print(physical_map)

# Calculate checksum
checksum = 0
for i, num in enumerate(physical_map):
    if num == '.':
        break
    else:
        checksum += i * int(num)

print(f"Checksum for part 1: {checksum}")

# Part two

## Read in input txt
with open("./09/input.txt", "r") as input:
    disk_map = input.read().strip()

physical_map = gen_physical_map(disk_map=disk_map)
file_sizes = Counter(physical_map)
processed_file_ids = []

curr_file_id = int(list(file_sizes.keys())[-1])

while True:
    curr_file_location = physical_map.index(str(curr_file_id))
    file_size = file_sizes[str(curr_file_id)]
    first_block = find_free_space(physical_map=physical_map, num_blocks=file_size)
    if first_block > -1 and first_block < curr_file_location:
        for _ in range(file_size):
            physical_map = swap_positions(curr_file_location, first_block, physical_map)
            curr_file_location += 1
            first_block += 1
    curr_file_id -= 1 
    if curr_file_id == 1:
        break

checksum = 0
for i, num in enumerate(physical_map):
    if num != '.':
        checksum += i * int(num)
print(f"Checksum for part 2: {checksum}")