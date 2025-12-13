def get_combo_operand(operand:int, reg_A:int, reg_B:int, reg_C:int) -> int:
    """
    returns the value of the operand
    """

    if operand == 0 or operand == 1 or operand == 2 or operand == 3:
        return operand
    elif operand == 4:
        return reg_A
    elif operand == 5:
        return reg_B
    elif operand == 6:
        return reg_C
    
    raise(ValueError("Invalid operand"))

def run_program(program:list, reg_A:int, reg_B:int, reg_C:int) -> list:
    """
    executes the program
    """

    curr_position = 0
    outputs = []

    # don't use a for-loop because of jumps
    while True:
        instr = program[curr_position]
        operand = program[curr_position + 1]

        # adv
        if instr == 0:
            operand = get_combo_operand(operand, reg_A, reg_B, reg_C)
            reg_A = int(reg_A/(2**operand))
        # bxl
        elif instr == 1:
            # literal operand
            reg_B = reg_B^operand
        # bst
        elif instr == 2:
            operand = get_combo_operand(operand, reg_A, reg_B, reg_C)
            reg_B = operand % 8
        # jnz
        elif instr == 3:
            if reg_A != 0:
                curr_position = operand
                continue
        # bxc
        elif instr == 4:
            reg_B = reg_B^reg_C
        # out
        elif instr == 5:
            operand = get_combo_operand(operand, reg_A, reg_B, reg_C)
            outputs.append(operand % 8)
        # bdv
        elif instr == 6:
            operand = get_combo_operand(operand, reg_A, reg_B, reg_C)
            reg_B = int(reg_A/(2**operand))
        # cdv
        elif instr == 7:
            operand = get_combo_operand(operand, reg_A, reg_B, reg_C)
            reg_C = int(reg_A/(2**operand))
        
        curr_position += 2
        if curr_position >= len(program):
            break

    return outputs, reg_A, reg_B, reg_C


def loop_through(program: list, min_reg_A: int, y: int) -> int:
    """
    loops through the range of reg_A values to find the correct one
    """

    possible_values = []

    for x in range(0,8):
        reg_A = min_reg_A + x*(8**(15-y)) 
        outputs, _, _, _ = run_program(program, reg_A, 0, 0)
        try:
            if outputs[-1-y:] == program[-1-y:]:
                possible_values.append(reg_A)
        except IndexError:
            pass
    return possible_values


# Tests
outputs, reg_A, reg_B, reg_C = run_program([2,6], 0, 0, 9)
assert reg_B == 1
outputs, reg_A, reg_B, reg_C = run_program([5,0,5,1,5,4], 10, 0, 0)
assert outputs == [0,1,2]
outputs, reg_A, reg_B, reg_C = run_program([0,1,5,4,3,0], 2024, 0, 0)
assert outputs == [4,2,5,6,7,7,7,7,3,1,0] and reg_A == 0
outputs, reg_A, reg_B, reg_C = run_program([1,7], 0, 29, 0)
assert reg_B == 26
outputs, reg_A, reg_B, reg_C = run_program([4,0], 0, 2024, 43690)
assert reg_B == 44354

# sample
outputs, reg_A, reg_B, reg_C = run_program([0,1,5,4,3,0], 729, 0, 0)
assert outputs == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]

# Part 1
program = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]
outputs, reg_A, reg_B, reg_C = run_program(program, 47792830, 0, 0)
print(",".join(map(str, outputs)))

 # Part 2
possible_values = [0]

for x in range(0,16):
    new_possible_values = []
    for value in possible_values:
        new_possible_values.extend(loop_through(program,value,x))
    possible_values = new_possible_values

min_value = min(possible_values)
outputs, reg_A, reg_B, reg_C = run_program(program,min_value, 0, 0)
assert outputs == program
print(f"Minimum value: {min_value}")