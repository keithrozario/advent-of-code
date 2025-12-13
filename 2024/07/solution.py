# # import sample text

# with open('./07/input.txt', 'r') as file:
#     lines = file.readlines()


# import itertools
# operators = '+*'
# matches = 0
# for line in lines:
#     result, nums = line.split(':')
#     nums = [int(x) for x in nums.strip().split(" ")]
#     operator_iterables = itertools.product(operators, repeat=len(nums)-1)    
    
#     # Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged.
#     for operator_iterable in operator_iterables:        
#         calc_result = nums[0]
#         for i, operator in enumerate(operator_iterable):
#             if operator == '+':
#                 calc_result += nums[i+1]
#             elif operator == '*':
#                 calc_result *= nums[i+1]
#         if int(result) == calc_result:
#             print(result)
#             matches += calc_result
#             break

# print(f"Total matches are: {matches}")

# ## Part 2


# """
# This part was interesting, instead of solving the equation mathematically (e.g. x10 and shift)
# It was solved as string, which was the 'domain' of the problem
# Solving problems in their own domain is a much more effective and efficient method
# """
# def concate(x: int, y: int) -> int:
#     return int(str(x) + str(y))

# operators = '+*~' # user tilde as drop in for ||

# matches = 0
# for line in lines:
#     result, nums = line.split(':')
#     nums = [int(x) for x in nums.strip().split(" ")]
#     operator_iterables = itertools.product(operators, repeat=len(nums)-1)    
    
#     # Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged.
#     for operator_iterable in operator_iterables:        
#         calc_result = nums[0]
#         for i, operator in enumerate(operator_iterable):
#             if operator == '+':
#                 calc_result += nums[i+1]
#             elif operator == '*':
#                 calc_result *= nums[i+1]
#             elif operator == '~':
#                 calc_result = concate(calc_result, nums[i+1])
#         if int(result) == calc_result:
#             print(result)
#             matches += calc_result
#             break

# print(f"Total matches are: {matches}")

## All below this line was refactored by Gemini

import itertools

def calculate(nums, operators):
    """Calculates the result of a series of operations on a list of numbers."""
    result = nums[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += nums[i+1]
        elif operator == '*':
            result *= nums[i+1]
        elif operator == '~':  # Concatenation operator for part 2
            result = int(str(result) + str(nums[i+1]))
    return result


def solve(lines, operators):
    """Solves the puzzle for a given set of lines and operators."""
    matches = 0
    for line in lines:
        target_result_str, num_string = line.split(':')
        target_result = int(target_result_str)
        nums = [int(x) for x in num_string.strip().split()]

        for operator_combination in itertools.product(operators, repeat=len(nums) - 1):
            calculated_result = calculate(nums, operator_combination)
            if target_result == calculated_result:
                matches += calculated_result
                break  # Stop searching for combinations once a match is found
    return matches


if __name__ == "__main__":
    with open('./07/input.txt', 'r') as file:
        lines = file.readlines()

    # Part 1
    part1_operators = '+*'
    part1_matches = solve(lines, part1_operators)
    print(f"Part 1: Total matches are: {part1_matches}")

    # Part 2
    part2_operators = '+*~'
    part2_matches = solve(lines, part2_operators)
    print(f"Part 2: Total matches are: {part2_matches}")

