
from typing import Tuple


starting_position = 50
num_total_position_on_dial = 100

def move_right(pos: int, num_clicks: int)->Tuple[int,int]:
    """
    moves the counter to the right.
    Args:
        pos: The current position of the dial
        num_clicks: The distance in number of clicks
    returns:
        new_pos: The new position
        zero_clicks: Number of times the click points to zero
    """

    # every full rotation will pass 0
    zero_clicks = int(num_clicks/num_total_position_on_dial)

    effective_shift = num_clicks % num_total_position_on_dial
    new_pos = (pos + effective_shift) % num_total_position_on_dial
    if new_pos < pos and pos != 0:
        zero_clicks += 1 # one more pass through 0, includes case for when new_pos==0
    
    return new_pos, zero_clicks

def move_left(pos: int, num_clicks: int)->Tuple[int,int]:
    """
    moves the counter to the left.
    Args:
        pos: The current position of the dial
        num_clicks: The distance in number of clicks
    returns:
        new_pos: The new position
        zero_clicks: Number of times the click points to zero
    """
    zero_clicks = int(num_clicks/num_total_position_on_dial)

    effective_shift = num_clicks % num_total_position_on_dial
    new_pos = (pos - effective_shift)
    if new_pos <=0 and pos != 0:
        zero_clicks += 1
    if new_pos < 0:
        new_pos += num_total_position_on_dial

    
    return new_pos,zero_clicks

def rotate(rotations: list)->int:
    pos = starting_position
    zero_count = 0 
    for r in rotations:
        if r[0] == "L":
            pos,zero_click = move_left(pos,int(r[1:]))
        else:
            pos,zero_click = move_right(pos,int(r[1:]))
        zero_count += zero_click
        # print(f"Moved {r[1:]} to position: {pos}, zero_count: {zero_count}")
    
    return zero_count

if __name__ == "__main__":

    # Tests
    assert move_left(99,2) == (97,0)
    assert move_right(99,2) ==(1,1)
    assert move_left(1,2) == (99,1)
    assert move_right(1,2) == (3,0)
    assert move_left(50,68) == (82,1)
    assert move_right(52,48) == (0,1)
    assert move_left(52,52) == (0,1)
    assert move_left(50,1000) == (50,10)
    assert move_right(50,1000) == (50,10)

    # Test on sample
    with open('./2025/01/sample.txt', 'r') as test_file:
        rotations = [line.strip() for line in test_file.readlines()]
    
    zero_count = rotate(rotations)
    print(f"Final Zero Count is {zero_count}")

    # Final input
    with open('./2025/01/input.txt', 'r') as test_file:
        rotations = [line.strip() for line in test_file.readlines()]
    
    zero_count = rotate(rotations)
    print(f"Final Zero Count is {zero_count}")
    
