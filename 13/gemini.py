import re
import numpy as np


file = "./13/input.txt"

def solve():
    with open(file, 'r') as f:
        machines = []
        machine_data = ""
        for line in f:
            if line.strip() == "":  # Empty line separates machines
                match = re.match(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", machine_data.strip())
                if match:
                    ax, ay, bx, by, px, py = map(int, match.groups())
                    machines.append(((ax, ay), (bx, by), (px, py)))
                machine_data = ""  # Reset for the next machine
            else:
                machine_data += line

        # Process the last machine if the file doesn't end with a blank line
        if machine_data:
            match = re.match(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", machine_data.strip())
            if match:
                ax, ay, bx, by, px, py = map(int, match.groups())
                machines.append(((ax, ay), (bx, by), (px, py)))

    def get_min_cost(machines, offset=0): # Added offset parameter
        min_costs = []
        for (ax, ay), (bx, by), (px, py) in machines:
            px += offset  # Apply offset for Part 2
            py += offset

            A = np.array([[ax, bx], [ay, by]])
            try:
                A_inv = np.linalg.inv(A)
                B = np.array([px, py])
                solution = np.dot(A_inv, B)
                a, b = solution.round().astype(int)  # Round to nearest integer

                if a >= 0 and b >= 0 and np.allclose(np.dot(A, [a, b]), [px, py]):  # Check validity
                    min_costs.append(3 * a + b)
                else:
                    min_costs.append(float('inf'))
            except np.linalg.LinAlgError:  # Handle singular matrices
                min_costs.append(float('inf'))
        return min_costs

    min_costs = get_min_cost(machines)
    total_cost = sum(cost for cost in min_costs if cost != float('inf'))
    print(total_cost)

    offset = 10000000000000
    min_costs_part2 = get_min_cost(machines, offset)  # Pass offset here
    total_cost_part2 = sum(cost for cost in min_costs_part2 if cost != float('inf'))
    print(total_cost_part2)

solve()