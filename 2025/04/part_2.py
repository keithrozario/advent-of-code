import numpy as np
import io
from scipy.signal import convolve2d
from typing import Tuple

def solve(grid_chars: np.ndarray) -> Tuple[np.ndarray,int]:

    # Convert the character grid to a numeric grid (1 for '@', 0 for '.')
    grid = (grid_chars == '@').astype(int)
    
    # The rest of the function remains the same
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    
    neighbor_counts = convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)
    
    rows, cols = np.where(grid == 1)
    
    total_rolls = 0
    for r, c in zip(rows, cols):
        if neighbor_counts[r,c] < 4:
            total_rolls += 1
            grid_chars[r][c] = 'x'
        # print(f"Cell at ({r}, {c}) has {neighbor_counts[r, c]} '@' neighbors.")

    return grid_chars, total_rolls

def iterate_roll_removal(starting_grid_char: np.ndarray):
    total_rolls = 0
    grid_chars = starting_grid_char
    while True:
        grid_chars, rolls = solve(grid_chars=grid_chars)
        total_rolls += rolls
        # print(f"Rolls this round: {rolls}")
        if rolls == 0:
            break
    return total_rolls

if __name__ == "__main__":

    grid_chars = np.genfromtxt("./2025/04/sample.txt",dtype='U1', delimiter=1)
    total_rolls = iterate_roll_removal(starting_grid_char=grid_chars)
    print(f"Final Total: {total_rolls}")

    grid_chars = np.genfromtxt("./2025/04/input.txt",dtype='U1', delimiter=1)
    total_rolls = iterate_roll_removal(starting_grid_char=grid_chars)
    print(f"Final Total: {total_rolls}")
    
