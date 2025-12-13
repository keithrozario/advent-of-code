def can_construct(design, patterns, memo):
    if design in memo:
        return memo[design]
    if design == "":
        return True

    for pattern in patterns:
        if design.startswith(pattern):
            suffix = design[len(pattern):]
            if can_construct(suffix, patterns, memo):
                memo[design] = True
                return True

    memo[design] = False
    return False

def count_possible_designs(patterns, designs):
    memo = {}
    count = 0
    for design in designs:
        
        if can_construct(design, patterns, memo):
            count += 1
    return count

def count_ways_to_construct(design, patterns, memo):
    if design in memo:
        return memo[design]
    if design == "":
        return 1

    total_ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            suffix = design[len(pattern):]
            total_ways += count_ways_to_construct(suffix, patterns, memo)

    memo[design] = total_ways
    return total_ways

def total_ways_to_construct_designs(patterns, designs):
    memo = {}
    total_ways = 0
    for design in designs:
        total_ways += count_ways_to_construct(design, patterns, memo)
    return total_ways

def get_input_data(file_name: str) -> tuple[list[str], list[str]]:
    with open(file_name, "r") as f:
        lines = f.readlines()
    patterns = [x.strip() for x in lines[0].split(",")]
    designs = [x.strip() for x in lines[2:]]

    return patterns, designs

# Sample Test
patterns, designs = get_input_data("./19/sample.txt")
possible_designs_count = count_possible_designs(patterns, designs)
assert possible_designs_count == 6

# Sample Test
patterns, designs = get_input_data("./19/sample.txt")
total_ways = total_ways_to_construct_designs(patterns, designs)
assert total_ways == 16

# Part 1
patterns, designs = get_input_data("./19/input.txt")
possible_designs_count = count_possible_designs(patterns, designs)
print(possible_designs_count)

# Part 2
patterns, designs = get_input_data("./19/input.txt")
total_ways = total_ways_to_construct_designs(patterns, designs)
print(total_ways)