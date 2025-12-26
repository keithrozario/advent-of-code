import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import re

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

def solve_joltage(line):
    button_matches = re.findall(r'\((.*?)\)', line)
    joltage_match = re.search(r'\{(.*?)\}', line)
    
    target = np.array([int(x) for x in joltage_match.group(1).split(',')]) # type: ignore
    num_buttons = len(button_matches)
    num_counters = len(target)
    
    # A Matrix: Counters x Buttons
    A = np.zeros((num_counters, num_buttons))
    for j, btn in enumerate(button_matches):
        for idx in btn.split(','):
            A[int(idx), j] = 1
            
    # Objective: Minimize sum(x)
    c = np.ones(num_buttons)
    
    # Constraints: Ax == target
    # milp uses LinearConstraint(A, lower_bound, upper_bound)
    constraints = LinearConstraint(A, target.astype(float), target.astype(float)) # pyright: ignore[reportArgumentType]
    
    # Integrality: 1 means must be integer
    integrality = np.ones(num_buttons)
    
    # Bounds: Buttons must be pressed >= 0 times
    bounds = Bounds(0, np.inf)
    
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    
    if res.success:
        return int(np.round(res.fun))
    return 0

if __name__ == "__main__":
    with open("./2025/10/sample.txt", "r") as sample_file:
        lines = sample_file.readlines()

    assert solve_joltage(lines[0]) == 10
    assert solve_joltage(lines[1]) == 12
    assert solve_joltage(lines[2]) == 11

    total = 0
    for line in lines:
        total += solve_joltage(line)
    print(total)

    with open("./2025/10/input.txt", "r") as input_file:
        lines = input_file.readlines()

    total = 0
    for line in lines:
        total += solve_joltage(line)
    print(total)
