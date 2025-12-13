def parse_input(input_data):
    initial_values = {}
    gates = []

    lines = input_data.strip().split('\n')
    for line in lines:
        if ':' in line:
            wire, value = line.split(': ')
            initial_values[wire] = int(value)
        elif len(line)>0:
            gates.append(line)

    return initial_values, gates

def evaluate_gate(gate, wire_values):
    parts = gate.split()
    input1 = wire_values[parts[0]]
    input2 = wire_values[parts[2]]
    output = parts[4]
    operation = parts[1]

    if operation == 'AND':
        wire_values[output] = input1 & input2
    elif operation == 'OR':
        wire_values[output] = input1 | input2
    elif operation == 'XOR':
        wire_values[output] = input1 ^ input2

def simulate_gates(initial_values, gates):
    wire_values = initial_values.copy()
    pending_gates = gates.copy()

    while pending_gates:
        for gate in pending_gates[:]:
            parts = gate.split()
            if parts[0] in wire_values and parts[2] in wire_values:
                evaluate_gate(gate, wire_values)
                pending_gates.remove(gate)

    return wire_values

def get_output_value(wire_values):
    binary_number = ''.join(str(wire_values[f'z{i:02}']) for i in range(len(wire_values)) if f'z{i:02}' in wire_values)

    z_keys = []
    for _ in wire_values.keys():
        if _.startswith('z'):
            z_keys.append(_)
    
    binary_num_str = []
    z_keys.sort(reverse=True)
    for key in z_keys:
       binary_num_str.append(str(wire_values[key]))
    
    base_10_num = int(''.join(binary_num_str), 2)
    
    return base_10_num

def main(input_data):
    initial_values, gates = parse_input(input_data)
    wire_values = simulate_gates(initial_values, gates)
    output_value = get_output_value(wire_values)
    return output_value

# Example usage
with open("./24/sample.txt", "r") as f:
    input_data = f.read()
output = main(input_data)
assert output == 2024

with open("./24/input.txt", "r") as f:
    input_data = f.read()
output = main(input_data)
print(output)