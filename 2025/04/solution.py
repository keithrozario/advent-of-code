
def solve():
    with open('/Users/krozario/projects/advent-of-code/2025/04/sample.txt', 'r') as f:
        grid = [list(line.strip()) for line in f]

    rows = len(grid)
    if rows == 0:
        print(0)
        return
    cols = len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                neighbors = 0
                # Check up
                if r > 0 and grid[r-1][c] == '@':
                    neighbors += 1
                # Check down
                if r < rows - 1 and grid[r+1][c] == '@':
                    neighbors += 1
                # Check left
                if c > 0 and grid[r][c-1] == '@':
                    neighbors += 1
                # Check right
                if c < cols - 1 and grid[r][c+1] == '@':
                    neighbors += 1
                
                if neighbors < 4:
                    count += 1
    print(count)

if __name__ == '__main__':
    solve()
