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

print(checksum)

# Part two