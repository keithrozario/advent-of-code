import galois
import numpy as np
import re

# Initialize the GF(2) field (Binary: 0 and 1)
GF2 = galois.GF(2)

def solve_machine(line):
    # 1. Parse Input
    # Example: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)
    diagram_match = re.search(r'\[(.*?)\]', line)
    button_matches = re.findall(r'\((.*?)\)', line)
    
    target_str = diagram_match.group(1)
    num_lights = len(target_str)
    
    # Target vector b (1 for #, 0 for .)
    b = GF2([1 if c == '#' else 0 for c in target_str])
    
    # Matrix A (each column is a button)
    button_list = []
    for btn in button_matches:
        vec = [0] * num_lights
        for idx in btn.split(','):
            vec[int(idx)] = 1
        button_list.append(vec)
    
    # Transpose so buttons are columns
    A = GF2(button_list).T 

    # 2. Solve Ax = b
    # We use row_reduce (Gaussian Elimination) to find the solution and null space
    augmented = np.hstack((A, b.reshape(-1, 1)))
    rref = augmented.row_reduce()
    
    # Separate the reduced matrix and the result column
    final_A = rref[:, :-1]
    final_b = rref[:, -1]
    
    # 3. Handle Free Variables for Minimum Presses
    # If the system is solvable, find a particular solution
    # and explore the null space to minimize 'sum(x == 1)'
    try:
        # solve() works if A is square and non-singular
        # For general cases, we find the null space
        x_particular = A.lstsq(b) 
        
        # If there's a null space, we add basis vectors to minimize bit count
        ns = A.null_space()
        
        if len(ns) == 0:
            return int(np.sum(x_particular))
        
        # Small brute force over null space combinations to minimize presses
        min_presses = int(np.sum(x_particular))
        for i in range(2**len(ns)):
            combination = x_particular.copy()
            for j in range(len(ns)):
                if (i >> j) & 1:
                    combination ^= ns[j]
            min_presses = min(min_presses, int(np.sum(combination)))
            
        return min_presses
    except:
        return 0 # Or handle unsolvable machine

# Example Usage
line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
print(f"Fewest presses: {solve_machine(line)}")