import numpy as np

def find_min_tokens(Ax, Ay, Bx, By, Px, Py):
    A = np.array([[Ax, Bx], [Ay, By]])
    P = np.array([Px, Py])
    
    try:
        solution = np.linalg.solve(A, P).round().astype(int)
        a, b = solution
        if a*Ax + b*Bx == Px and a*Ay + b*By == Py:
            tokens = int(a) * 3 + int(b) * 1
            return tokens
    except np.linalg.LinAlgError:
        pass
    
    return None

def get_machines(filename: str):

    machines = []

    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i in range(0, len(lines), 4):
        config = lines[i].split("+")
        A = (int(config[1].split(",")[0]),int(config[2]))
        config = lines[i+1].split("+")
        B = (int(config[1].split(",")[0]), int(config[2]))
        config = lines[i+2].split("=")
        P = (int(config[1].split(",")[0]), int(config[2]))

        machines.append(
            {
                "A": A,
                "B": B,
                "P": P
            }
        )

    return machines

def min_tokens_to_win_prizes(machines, offset:int=0):
    total_tokens = 0
    prizes_won = 0

    for machine in machines:
        Ax, Ay = machine['A']
        Bx, By = machine['B']
        Px, Py = machine['P']
        Px += offset
        Py += offset
        min_tokens = find_min_tokens(Ax, Ay, Bx, By, Px, Py)
        if min_tokens is not None:
            total_tokens += min_tokens
            prizes_won += 1

    return prizes_won, total_tokens

# Example usage
machines = get_machines('13/input.txt')

prizes_won, total_tokens = min_tokens_to_win_prizes(machines)
print(f"Prizes won: {prizes_won}, Total tokens: {total_tokens}")

prizes_won, total_tokens = min_tokens_to_win_prizes(machines, offset=10000000000000)
print(f"Prizes won: {prizes_won}, Total tokens: {total_tokens}")
