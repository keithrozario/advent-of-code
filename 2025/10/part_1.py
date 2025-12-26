import re
from collections import deque

def get_mask(line: str)->int:
    """
    Returns target mask e.g. (011) as an integer (3)
    Args:
        line: String of the line in the input
    """
    target_str = line.split("]")[0][1:]

    # Convert target to a bitmask (e.g., "#.#" -> 101 in binary -> 5)
    target_mask = 0
    for i, char in enumerate(target_str):
        if char == '#':
            target_mask |= (1 << i)
    
    return target_mask


def get_buttons(line: str)->list:
    """
    Returns a list of integer reprensentation of the button
    e.g. (3) = 1000 = 8, (1,3) = 1010 = 10, (0,2) = 0101 = 3
    Args:
        line: String of the line in the input
    """

    button_matches = re.findall(r'\((.*?)\)', line)
    buttons = []
    for btn in button_matches:
        mask = 0
        for idx in btn.split(','):
            mask |= (1 << int(idx))
        buttons.append(mask)
    
    return buttons



def solve_machine_bfs(target_mask: int, buttons: list) -> int:
    queue = deque([(0, 0, -1)])
    visited = {0}
    
    while queue:
        curr_mask, presses, last_idx = queue.popleft()
        
        if curr_mask == target_mask:
            return presses

        for i in range(last_idx + 1, len(buttons)):
            next_mask = curr_mask ^ buttons[i]
            if next_mask not in visited:
                visited.add(next_mask)
                queue.append((next_mask, presses + 1, i))
                
    return 0

def process_line(line: str)->int:
    target_mask = get_mask(line)
    buttons = get_buttons(line)
    fewest_presses = solve_machine_bfs(target_mask=target_mask, buttons=buttons)
    return fewest_presses


if __name__ == "__main__":

    assert(process_line("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")) == 2
    assert(process_line("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}")) == 3
    assert(process_line("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}")) == 2

    with open("./2025/10/sample.txt","r") as sample_file:
        lines = sample_file.readlines()
    total = 0 
    for line in lines:
        total += process_line(line)
    print(total)

    with open("./2025/10/input.txt","r") as input_file:
        lines = input_file.readlines()
    total = 0 
    for line in lines:
        total += process_line(line)
    print(total)