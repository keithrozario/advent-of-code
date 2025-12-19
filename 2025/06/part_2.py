from typing import List
import numpy as np

def add_all_numbers(numbers: List[int])->int:
    total = 0
    for number in numbers:
        total += number
    return total

def multiply_all_numbers(numbers: List[int])->int:
    total = 1
    for number in numbers:
        total *= number
    return total

def get_problem_sets_in_2d(lines_from_file: list) -> List[list]:
    """
    Parses lines from a file, identifies problem sets separated by string-only columns,
    and returns them as a list of 2D numpy arrays.
    """
    # Convert list of strings to a 2D list of characters
    problems_in_2d_list = [list(line.rstrip('\n')) for line in lines_from_file]
    problems_in_2d_np = np.array(problems_in_2d_list)

    # Find columns that consist only of strings (non-digits)
    is_not_digit = ~np.char.isdigit(problems_in_2d_np)
    string_only_cols_indices = np.where(is_not_digit.all(axis=0))[0]
    
    string_only_cols_indices = np.append(string_only_cols_indices, [len(problems_in_2d_list[0])])
    problem_sets = []
    start_col = 0
    # Use the delimiter indices to slice the original list of lists
    for end_col in string_only_cols_indices:
        # Slice each row from start_col to end_col
        problem_set = [row[start_col:end_col] for row in problems_in_2d_list]
        problem_sets.append(problem_set)
        start_col = end_col + 1

    return problem_sets


def apply_cephalapod_logic(problem_set: list)->list:
    """
    Applies Cephalapod logic to the problem set to get the
    numbers
    """

    dummy_char = ' '
    cephalapod_numbers = []
    for col in range(len(problem_set[0])):
        num = ''
        for row in range(len(problem_set)-1):
            char = problem_set[row][col]
            if char != dummy_char:
                num += char
        cephalapod_numbers.append(int(num))
    return cephalapod_numbers


def sum_problem_sets(problem_sets: list)->int:
    total = 0
    for problem_set in problem_sets:
        cephalapod_numbers = apply_cephalapod_logic(problem_set)
        if '+' in problem_set[-1]:
            total += add_all_numbers(cephalapod_numbers)
        if '*' in problem_set[-1]:
            total += multiply_all_numbers(cephalapod_numbers)
    return total


if __name__ == "__main__":
    assert(add_all_numbers([1,2,3,4])) == 10
    assert(multiply_all_numbers([1,2,3,4])) == 24

    with open("./2025/06/sample.txt", "r") as sample_file:
        sample_lines = sample_file.readlines()
    problem_sets = get_problem_sets_in_2d(sample_lines)
    total = sum_problem_sets(problem_sets=problem_sets)
    assert total == 3263827

    with open("./2025/06/input.txt", "r") as input_file:
        input_lines = input_file.readlines()
    problem_sets = get_problem_sets_in_2d(input_lines)
    total = sum_problem_sets(problem_sets=problem_sets)
    print(total)