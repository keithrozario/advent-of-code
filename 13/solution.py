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

import numpy as np
from numpy.linalg import inv

def calculate_pushes(a_x, b_x, a_y, b_y, prize_x, prize_y) -> tuple[int, int]:
    """
    Using matrix multiplication
    if A . [x,y] = [prize_x, prize_y]
    then [x,y] = A^-1 . [prize_x, prize_y[]
    """

    A = np.array([[a_x,b_x],[a_y,b_y]])
    P = np.array([prize_x,prize_y])
    a_pushes, b_pushes = np.linalg.solve(A, P).round().astype(int)

    ## double check integer versions work
    if (a_x*a_pushes + b_x*b_pushes) == prize_x and (a_y*a_pushes + b_y*b_pushes) == prize_y:
        return (a_pushes, b_pushes)
    else:
        return (None, None)

def get_config(machine_config: dict):

    a_x = machine_config["A"]["X"]
    b_x = machine_config["B"]["X"]

    a_y = machine_config["A"]["Y"]
    b_y = machine_config["B"]["Y"]

    prize_x = machine_config["prize"]["X"]
    prize_y = machine_config["prize"]["Y"]

    return a_x, b_x, a_y, b_y, prize_x, prize_y


# part 1
machines = get_machines('./13/input.txt')

total_tokens = 0

for machine_num, machine_config in enumerate(machines):

    a_x, b_x, a_y, b_y, prize_x, prize_y = get_config(machine_config)

    machine_tokens_per_round = []
    for i in range(100):
        a_pushes = i
        for j in range(100):
            b_pushes = j
            if (a_pushes*a_x + b_pushes*b_x) == prize_x and \
               (a_pushes*a_y + b_pushes*b_y) == prize_y:
                machine_tokens_per_round.append(a_pushes*3 + b_pushes*1)
                # print(f"{machine_num}. a_pushes: {a_pushes}, b_pushes: {b_pushes}, tokens = {a_pushes*3 + b_pushes*1}")
    
    try:
        total_tokens += min(machine_tokens_per_round)
    except ValueError:
        # print(f"{machine_num}. No combination Found")
        pass

print(f"\n Total tokens: {total_tokens}")

# Part 2:
total_tokens = 0

for machine_num, machine_config in enumerate(machines):

    a_x, b_x, a_y, b_y, prize_x, prize_y = get_config(machine_config)
    prize_x = 10000000000000 + prize_x
    prize_y = 10000000000000 + prize_y

    a_pushes, b_pushes = calculate_pushes(a_x, b_x, a_y, b_y, prize_x, prize_y)
    if a_pushes is not None:
        machine_tokens = a_pushes*3 + b_pushes*1
        # print(f"{machine_num}. a_pushes: {a_pushes}, b_pushes: {b_pushes}, tokens = {machine_tokens}")
        total_tokens += machine_tokens

print(f"\n Total tokens: {total_tokens}")