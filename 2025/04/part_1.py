import itertools

def read_grid(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def count_neighbors(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    neighbor_count = 0
    
    # Directions: 8 directions (including diagonals)
    for dr, dc in itertools.product(range(-1, 2), repeat=2):
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
            neighbor_count += 1
            
    return neighbor_count

def solve(filename):
    grid = read_grid(filename)

    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '@':
                if count_neighbors(grid, r, c) < 4:
                    # print(f"{r},{c} has count less of {count_neighbors(grid, r, c)}")
                    count += 1
    print(count)

if __name__ == '__main__':
    solve('/Users/krozario/projects/advent-of-code/2025/04/sample.txt')
    solve('/Users/krozario/projects/advent-of-code/2025/04/input.txt')