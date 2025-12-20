from typing import List

def calculate_splits(map: List[list])->int:
    total_splits = 0
    for row, line in enumerate(map):
        for col, cell in enumerate(line):
            if map[row-1][col] == "S":
                map[row][col] = "|"
            elif cell == "^":
                if map[row-1][col] == "|":
                    map[row][col+1] = "|"
                    map[row][col-1] = "|"
                    total_splits += 1
            elif map[row-1][col] == '|':
                map[row][col] = "|"
    return total_splits    


if __name__ == "__main__":
    with open("./2025/07/sample.txt", 'r') as sample_file:
        map = [list(line.strip()) for line in sample_file.readlines()]

    assert calculate_splits(map) == 21

    with open("./2025/07/input.txt", 'r') as input_file:
        map = [list(line.strip()) for line in input_file.readlines()]
    
    total_splits = calculate_splits(map)
    print(total_splits)
