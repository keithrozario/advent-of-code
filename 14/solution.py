import numpy as np

def parse_input(file_name: str) -> list:
    with open(file_name) as f:
        input_text = f.read()
    
    lines = input_text.strip().split('\n')
    robots = []

    for line in lines:
        x_start = int(line.split(",")[0].split("=")[1])
        y_start = int(line.split(",")[1].split(" ")[0])
        v_x = int(line.split(",")[1].split("=")[1])
        v_y = int(line.split(",")[2])
        robots.append((x_start, y_start, v_x, v_y))
    
    return robots

def simulate_robots(robots, width, height, seconds):
    positions = [(x, y) for x, y, _, _ in robots]
    velocities = [(v_x, v_y) for _, _, v_x, v_y in robots]

    for _ in range(seconds):
        new_positions = []
        for (x, y), (v_x, v_y) in zip(positions, velocities):
            new_x = (x + v_x) % width
            new_y = (y + v_y) % height
            new_positions.append((new_x, new_y))
        positions = new_positions

    return positions

def count_robots_in_quadrants(positions, width, height):
    mid_x = width // 2
    mid_y = height // 2

    quadrants = [0, 0, 0, 0]

    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            quadrants[0] += 1
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1
        elif x >= mid_x and y >= mid_y:
            quadrants[3] += 1

    return quadrants

def get_safety_factor(robots, width, height, seconds):
    positions = simulate_robots(robots, width, height, seconds)
    quadrants = count_robots_in_quadrants(positions, width, height)
    safety_factor = np.prod(quadrants)
    return safety_factor

robots = parse_input(file_name='./14/input.txt')
width, height = 101, 103
max_seconds = 100  # Adjust this value as needed
safety_factor = get_safety_factor(robots, width, height, max_seconds)
print(safety_factor)