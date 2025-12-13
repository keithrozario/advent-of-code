
starting_position = 50
num_total_position_on_dial = 100

def move_right(pos: int, num_clicks: int)->int:
    """
    moves the counter to the right.
    Args:
        pos: The current position of the dial
        num_clicks: The distance in number of clicks
    returns:
        new_pos: The new position
    """
    effective_shift = num_clicks % 100
    new_pos = (pos + effective_shift) % num_total_position_on_dial
    return new_pos

def move_left(pos: int, num_clicks: int)->int:
    """
    moves the counter to the left.
    Args:
        pos: The current position of the dial
        num_clicks: The distance in number of clicks
    returns:
        new_pos: The new position
    """
    effective_shift = num_clicks % 100
    new_pos = (pos - effective_shift)
    if new_pos < 0:
        new_pos += 100
    return new_pos

def rotate(rotations: list)->int:
    pos = starting_position
    zero_count = 0 
    for r in rotations:
        if r[0] == "L":
            pos = move_left(pos,int(r[1:]))
        elif r[0] == "R":
            pos = move_right(pos,int(r[1:]))
        if pos == 0:
            zero_count += 1
        # print(f"Moved {r[1:]} to position: {pos}")
    
    return zero_count

if __name__ == "__main__":

    # Tests
    assert move_left(99,2) == 97
    assert move_right(99,2) == 1
    assert move_left(1,2) == 99
    assert move_right(1,2) == 3
    assert move_left(50,68) == 82
    assert move_right(52,48) == 0
    assert move_left(52,52) == 0

    # Test on sample
    with open('./2025/01/sample.txt', 'r') as test_file:
        rotations = [line.strip() for line in test_file.readlines()]
    
    zero_count = rotate(rotations)
    print(f"Final Zero Count is {zero_count}")

    with open('./2025/01/input.txt', 'r') as test_file:
        rotations = [line.strip() for line in test_file.readlines()]
    
    zero_count = rotate(rotations)
    print(f"Final Zero Count is {zero_count}")
    
