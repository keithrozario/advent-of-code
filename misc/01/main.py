"""
A bee lands on a clock at the 12 o' clock position.
The bee moves one step randomly, either clockwise or counter-clockwise
It continues moving one step at a time till it has visited all hour positions
What is the probability that last hour position it visited was 6 o'clock
"""

import random
from collections import Counter


positions = [12,1,2,3,4,5,6,7,8,9,10,11]

def move(curr_index: int)->int:
    
    move = random.choice([1, -1])
    new_index = (curr_index+move) % len(positions)

    return new_index

def get_last_visited():
    visited = set()
    curr_index = 0
    last_visited = -1
    while len(visited)<len(positions):
        clock_position = positions[curr_index]
        if clock_position not in visited:
            visited.add(clock_position)
            last_visited = clock_position
        curr_index = move(curr_index=curr_index)
    
    return last_visited

if __name__ == "__main__":
    TOTAL_RUNS = 100000
    last_visited_positions = []
    for _ in range(TOTAL_RUNS):
        last_visited_positions.append(get_last_visited())
    
    counts = Counter(last_visited_positions)
    print(f"Running {TOTAL_RUNS} simulations...")
    for k in sorted(counts.keys()):
        probability = counts[k] / TOTAL_RUNS
        print(f"Position {k}: {probability:.4f}")