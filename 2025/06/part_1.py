from typing import List

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

def get_problems_in_2d(lines_from_file: list)->List[list]:
    """ 
    Returns the file as a 2d list, where each row corresponds to a row in the file
    and each row is a list of numbers/operators in the line
    """
    
    problems_in_2d = []
    for line in lines_from_file:
        line_items = list(filter(lambda x: x not in('','\n'),line.split(" ")))
        try:
            line_integers = [int(x.strip()) for x in line_items]
            problems_in_2d.append(line_integers)
        except ValueError:
            # last line of operators
            problems_in_2d.append(line_items)

    return problems_in_2d


def get_problem_sets(problems_in_2d: List[list])->List[list]:
    problem_sets = []
    for x in range(len(problems_in_2d[0])):
        problem_set = []
        for y in range(len(problems_in_2d)):
            problem_set.append(problems_in_2d[y][x])
        problem_sets.append(problem_set)
    
    return problem_sets

def sum_problem_sets(problem_sets: list)->int:
    total = 0
    for problem_set in problem_sets:
        if problem_set[-1] == "+":
            total += add_all_numbers(problem_set[:-1])
        if problem_set[-1] == "*":
            total += multiply_all_numbers(problem_set[:-1])
    return total


if __name__ == "__main__":
    assert(add_all_numbers([1,2,3,4])) == 10
    assert(multiply_all_numbers([1,2,3,4])) == 24


    with open("./2025/06/sample.txt", "r") as sample_file:
        sample_lines = sample_file.readlines()

    problems_in_2d = get_problems_in_2d(sample_lines)
    problem_sets=get_problem_sets(problems_in_2d)
    total = sum_problem_sets(problem_sets)
    assert total == 4277556

    with open("./2025/06/input.txt", "r") as sample_file:
        sample_lines = sample_file.readlines()

    problems_in_2d = get_problems_in_2d(sample_lines)
    problem_sets=get_problem_sets(problems_in_2d)
    total = sum_problem_sets(problem_sets)
    print(total)