import re

def solve_claw_machines_fast(machines, offset=0):
    """
    Calculates the maximum number of prizes you can win and the minimum total tokens spent using a faster approach.

    Args:
        machines: A list of strings, where each string represents a claw machine's configuration.

    Returns:
        A tuple: (number of winnable prizes, total tokens spent)
    """

    def solve_machine(machine_config):
        """Solves for a single machine and returns the minimum cost to win, or None if unwinnable."""
        a_x = machine_config["A"]["X"]
        b_x = machine_config["B"]["X"]

        a_y = machine_config["A"]["Y"]
        b_y = machine_config["B"]["Y"]

        prize_x = machine_config["prize"]["X"]
        prize_y = machine_config["prize"]["Y"]

        prize_x += offset
        prize_y += offset

        det = a_x * b_y - a_y * b_x

        if det == 0:
            return None  # No unique solution

        a_numerator = prize_x * b_y - prize_y * b_x
        b_numerator = a_x * prize_y - a_y * prize_x

        if a_numerator % det != 0 or b_numerator % det != 0:
            return None  # No integer solutions

        a = a_numerator // det
        b = b_numerator // det

        # Removed the check for 0 <= a <= 100 and 0 <= b <= 100
        return a * 3 + b * 1

    winnable_prizes = 0
    total_tokens = 0
    for machine in machines:
        cost = solve_machine(machine)
        if cost is not None:
            winnable_prizes += 1
            total_tokens += cost

    return winnable_prizes, total_tokens

# Example usage (replace with your actual input)
def get_machines(filename: str):

    machines = []

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i in range(0, len(lines), 4):
        config = lines[i].split("+")
        A = {
            "X": int(config[1].split(",")[0]),
            "Y": int(config[2])
        }
        config = lines[i+1].split("+")
        B = {
            "X": int(config[1].split(",")[0]),
            "Y": int(config[2])
        }
        config = lines[i+2].split("=")
        prize = {
            "X": int(config[1].split(",")[0]),
            "Y": int(config[2])
        }

        machines.append(
            {
                "A": A,
                "B": B,
                "prize": prize
            }
        )

    return machines

machines = get_machines("13/input.txt")
winnable_prizes, total_tokens = solve_claw_machines_fast(machines)
winnable_prizes, total_tokens = solve_claw_machines_fast(machines= machines, offset=10000000000000)
print(f"Winnable prizes: {winnable_prizes}")
print(f"Total tokens spent: {total_tokens}")