# import re
import numpy as np
import re

# get input
with open('./04/input.txt', 'r') as input:
    lines = [line.strip() for line in input.readlines()]

"""
This word search allows words to be horizontal, vertical, diagonal, written backwards
"""

xmas_count = 0
pattern = re.compile('XMAS')
reverse_pattern = re.compile('SAMX')

# HORIZONTAL
for i, line in enumerate(lines):
    xmas_count += len(pattern.findall(line))
    print(f"Counted Horizontal Instances on line {i}: {len(pattern.findall(line))}")
    xmas_count += len(reverse_pattern.findall(line))
    print(f"Counted Horizontal Reversed Instances on line {i}: {len(reverse_pattern.findall(line))}")

# VERTICAL
## Initialize list of columns
columns = [[] for _ in lines[0]]

## create list of columns, each containing columnar data
for y,line in enumerate(lines):
    for x, column in enumerate(columns):
        columns[x].append(line[x])

for i, column in enumerate(columns):
    xmas_count += len(pattern.findall(''.join(column)))
    print(f"Counted Vertical Instances on column {i}: {len(pattern.findall(''.join(column)))}")
    xmas_count += len(reverse_pattern.findall(''.join(column)))
    print(f"Counted Vertical Reversed Instances on column {i}: {len(reverse_pattern.findall(''.join(column)))}")

# DIAGONAL

xmas_2d_array = np.array([list(line) for line in lines])
# flips the array for right to left diagonals
xmas_2d_array_flipped = np.fliplr(xmas_2d_array)

for offset in range(-139,139):
    diagonal = xmas_2d_array.diagonal(offset=offset)
    diagonal_string = ''.join(diagonal.tolist())

    xmas_count += len(pattern.findall(diagonal_string))
    print(f"Counted Diaganol Instances on Diagonal {offset}: {len(pattern.findall(diagonal_string))}") 
    xmas_count += len(reverse_pattern.findall(diagonal_string))
    print(f"Counted Diaganol Reversed Instances on Diagonal {offset}: {len(reverse_pattern.findall(diagonal_string))}") 

    diagonal = xmas_2d_array_flipped.diagonal(offset=offset)
    diagonal_string = ''.join(diagonal.tolist())

    xmas_count += len(pattern.findall(diagonal_string))
    print(f"Counted Diaganol Instances on flipped Diagonal {offset}: {len(pattern.findall(diagonal_string))}") 
    xmas_count += len(reverse_pattern.findall(diagonal_string))
    print(f"Counted Diaganol Reversed Instances on flipped Diagonal {offset}: {len(reverse_pattern.findall(diagonal_string))}") 


print(f"\n\nCount of XMAS in puzzle {xmas_count}")


## PART 2


def check_sub_matrix(sub_matrix):
    """
    Returns 1 if there is an x-mas. Otherwise 0.
    """
    x_mas_pattern = ('MAS','SAM')
    diagonal_left = ''.join(list(sub_matrix.diagonal()))
    diagonal_right = ''.join(list(np.fliplr(sub_matrix).diagonal()))
    
    if diagonal_left in x_mas_pattern:
        if diagonal_right in x_mas_pattern:
            return 1

    return 0


# get input
with open('./04/test.txt', 'r') as input:
    lines = [line.strip() for line in input.readlines()]
    text = np.array([list(line) for line in lines])

mas_count = 0

# loop through matrix for each 3x3 submatrix
# each sub matrix can have at most 1 x-mas
for y in range(len(lines)-2):
    for x in range(len(lines[0])-2):
        sub_matrix = text[y:y+3, x:x+3]
        mas_count += check_sub_matrix(sub_matrix)

print(f"Count of X-MAS in puzzle {mas_count}")

