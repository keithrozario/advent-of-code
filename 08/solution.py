def parse_map(map_str):
    antennas = []
    lines = map_str.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                antennas.append((x, y, char))
    return antennas, len(lines), len(lines[0])

def calculate_antinodes(antennas, height, width):
    

def count_unique_antinodes(map_str):
    antennas, height, width = parse_map(map_str)
    antinodes = calculate_antinodes(antennas, height, width)
    return len(antinodes)

# Example usage
map_str = """
..........
..........
..........
....a.....
........a.
.....a....
..........
..........
..........
..........
"""

print(count_unique_antinodes(map_str))