def parse_machine(lines):
    """Parse a single machine's configuration from 3 lines of text."""
    button_a = lines[0].split(': ')[1].split(', ')
    button_b = lines[1].split(': ')[1].split(', ')
    prize = lines[2].split(': ')[1].split(', ')
    
    return {
        'a_x': int(button_a[0][2:]),
        'a_y': int(button_a[1][2:]),
        'b_x': int(button_b[0][2:]),
        'b_y': int(button_b[1][2:]),
        'prize_x': int(prize[0][2:]),
        'prize_y': int(prize[1][2:])
    }

def extended_gcd(a, b):
    """Return (g, x, y) where g = gcd(a, b) and g = a*x + b*y"""
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def solve_linear_equation(a, b, c):
    """Solve equation ax + by = c. Returns (x0, y0, d) where d is the gcd."""
    g, x, y = extended_gcd(abs(a), abs(b))
    if c % g != 0:
        return None  # No solution exists
    
    x0 = x * (c // g)
    y0 = y * (c // g)
    
    if a < 0: x0 = -x0
    if b < 0: y0 = -y0
    
    return x0, y0, abs(b) // g

def find_solution(machine):
    """Find solution using linear Diophantine equations."""
    a_x, b_x = machine['a_x'], machine['b_x']
    a_y, b_y = machine['a_y'], machine['b_y']
    target_x, target_y = machine['prize_x'], machine['prize_y']
    
    # Solve for X coordinate
    x_solution = solve_linear_equation(a_x, b_x, target_x)
    if not x_solution:
        return None
    x0, y0, tx = x_solution
    
    # Solve for Y coordinate
    y_solution = solve_linear_equation(a_y, b_y, target_y)
    if not y_solution:
        return None
    x1, y1, ty = y_solution
    
    # Find the smallest non-negative solution
    min_tokens = float('inf')
    best_solution = None
    
    # We need to try different combinations until we find matching X and Y solutions
    for k1 in range(-1000, 1000):
        a_presses = x0 + k1 * tx
        if a_presses < 0:
            continue
            
        b_presses = y0 - k1 * ty
        if b_presses < 0:
            continue
            
        # Verify this solution works for both X and Y
        if (a_presses * a_x + b_presses * b_x != target_x or 
            a_presses * a_y + b_presses * b_y != target_y):
            continue
            
        tokens = calculate_tokens(a_presses, b_presses)
        if tokens < min_tokens:
            min_tokens = tokens
            best_solution = (int(a_presses), int(b_presses))
    
    return best_solution

def calculate_tokens(a_presses, b_presses):
    """Calculate total tokens needed given number of button presses."""
    return a_presses * 3 + b_presses * 1

def solve_claw_machines(input_text):
    # Split input into machines
    lines = input_text.strip().split('\n')
    machines = []
    for i in range(0, len(lines), 4):
        if i + 2 < len(lines):
            machines.append(parse_machine(lines[i:i+3]))
    
    total_tokens = 0
    winnable_prizes = 0
    
    for machine in machines:
        solution = find_solution(machine)
        if solution:
            winnable_prizes += 1
            tokens = calculate_tokens(solution[0], solution[1])
            total_tokens += tokens
    
    return winnable_prizes, total_tokens

# Test with example input
with open("./13/input.txt") as f:
    input = f.read()

prizes, tokens = solve_claw_machines(input)
print(f"Winnable prizes: {prizes}")
print(f"Total tokens needed: {tokens}")