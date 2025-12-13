def get_key(batch: list) -> tuple:
    """
    Returns the height of #'s for each column in the key as a 5-tuple
    
    Example:
    .....
    #....
    #....
    #...#
    #.#.#
    #.###
    #####
    
    Returns: (5,1,2,2,3)
    """
    # Initialize counts for each column
    heights = [0] * 5
    
    # For each column
    for col in range(5):
        # Start from bottom row (excluding bottom row since it's always #####)
        # Batches will also include a empty line below each key/lock.
        for row in range(len(batch)-3, -1, -1):
            if batch[row][col] == '#':
                heights[col] += 1
            else:
                # Stop counting this column when we hit a '.'
                break
                
    return tuple(heights)

def get_lock(batch: list) -> tuple:
    """
    Returns the height of #'s for each column in the key as a 5-tuple
    
    Example:
    #####
    .####
    .####
    .####
    .#.#.
    .#...
    .....

    
    Returns: (0,5,3,4,3)
    """

    # Initialize counts for each column
    heights = [0] * 5
    
    # For each column
    for col in range(5):
        # Start from top row (excluding top row since it's always #####)
        # Batches will also include a empty line below each key/lock.
        for row in range(1, len(batch)):
            if batch[row][col] == '#':
                heights[col] += 1
            else:
                # Stop counting this column when we hit a '.'
                break
                
    return tuple(heights)


def process_batches(file_path)->list:
    
    locks = []
    keys = []
    with open(file_path, 'r') as file:
        all_lines = [line.strip() for line in file.readlines()]
        batches = [all_lines[i:i+8] for i in range(0, len(all_lines), 8)]

        
        for batch in batches:                
            if batch[0][0] == '#':
                locks.append(get_lock(batch))
            elif batch[0][0] == '.':
                keys.append(get_key(batch))
            else:
                raise ValueError("Invalid batch")
    
    return (locks, keys)

def check_lock_fit(lock: tuple, key: tuple)->bool:
    """
    Returns True if the key fits the lock, False otherwise
    """
    for i, col in enumerate(lock):
        if key[i] + col > 5:
            return False

    return True

def check_locks_and_keys(locks: list, keys: list)->int:
    """
    Returns the number of keys that fit the locks
    """
    count = 0
    for lock in locks:
        for key in keys:
            if check_lock_fit(lock, key):
                count += 1
    return count    

# Tests
locks, keys = process_batches('./25/sample.txt')
assert locks == [(0, 5, 3, 4, 3), (1, 2, 0, 5, 3)]
assert keys == [(5, 0, 2, 1, 3), (4, 3, 4, 0, 2), (3, 0, 2, 0, 1)]
assert check_locks_and_keys(locks=locks, keys=keys) == 3

# Part 1
locks, keys = process_batches('./25/input.txt')
matches = check_locks_and_keys(locks=locks, keys=keys)
print(f"Part 1: {matches}")