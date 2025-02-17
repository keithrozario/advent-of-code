import numpy as np

def count_paths_and_ratings(grid: np.array, target_val: int, start_val: int) -> tuple[int, int]:
    """Counts reachable targets and unique paths from start to target values in a grid."""

    rows, cols = grid.shape

    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols

    def dfs(row, col, current_val, reachable_targets, num_ratings):
        if grid[row, col] == target_val:
            reachable_targets.add((row, col))
            return reachable_targets, num_ratings + 1  # Return updated values

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if is_valid(new_row, new_col) and grid[new_row, new_col] == current_val + 1:
                reachable_targets, num_ratings = dfs(new_row, new_col, current_val + 1, reachable_targets, num_ratings) # receive updated values

        return reachable_targets, num_ratings  # Return current values if no target found


    total_reachable_targets = 0
    total_num_ratings = 0  # Initialize outside the loop

    for start_location in np.argwhere(grid == start_val):
        reachable_targets = set()
        reachable_targets, num_ratings = dfs(start_location[0], start_location[1], start_val, reachable_targets, 0) #pass initial values to DFS
        total_reachable_targets += len(reachable_targets)
        total_num_ratings += num_ratings # accumulate total path count

    return total_reachable_targets, total_num_ratings


# Example usage:
with open('./10/input.txt', 'r') as input:
    lines = [line.strip() for line in input.readlines()]
    grid_np = np.array([list(line) for line in lines]).astype(int)

target_val = 9
start_val = 0
num_paths, num_ratings = count_paths_and_ratings(grid_np, target_val, start_val)

# Part 1
print(f"Number of reachable {target_val}s from all {start_val}s : {num_paths}")

# Part 2
print(f"Number of ratings (unique paths): {num_ratings}")

### Note ####
"""
I used Gemini assist for most of this, modifying tiny bits along the way. I didn't copy paste the question.
Instead I chatted with Gemini about recursion and using numpy arrays, befor crafting the prompt and entering.

It was my misunderstanding that I understood part 1 to calculate unique paths (which was what part 2 asked for)

Gemini doesn't naturally use Numpy for these problems, unless prompted to. And even when it uses numpy does not use
Numpy capabilities liek np.argwhere().

Gemini also had a habit of spitting out bad code that either wouldn't run or gave wrong answers. But over time it got better.

Total time to complete this challenge was slightly less than 1 hour.

LLMs also generally do not use external packages .... 
https://huggingface.co/spaces/jerpint/advent24-llm/tree/main/day10

hmmm......
"""