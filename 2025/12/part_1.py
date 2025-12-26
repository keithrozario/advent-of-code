import os
import re

import sys
sys.setrecursionlimit(20000)

def get_rotations_and_flips(shape_coords):
    def rotate(coords):
        return [(-x, y) for y, x in coords]
    def flip(coords):
        return [(y, -x) for y, x in coords]
    def normalize(coords):
        min_y = min(y for y, x in coords)
        min_x = min(x for y, x in coords)
        return tuple(sorted((y - min_y, x - min_x) for y, x in coords))

    symmetries = set()
    curr = shape_coords
    for _ in range(4):
        symmetries.add(normalize(curr))
        symmetries.add(normalize(flip(curr)))
        curr = rotate(curr)
    return list(symmetries)

def can_place(grid, shape, r, c, W, H):
    for dr, dc in shape:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < H and 0 <= nc < W) or grid[nr][nc]:
            return False
    return True

def place(grid, shape, r, c, val):
    for dr, dc in shape:
        grid[r + dr][c + dc] = val

def can_fit(grid, remaining_shapes, all_presents, W, H):
    if not remaining_shapes:
        return True

    # First Empty Slot Heuristic
    r, c = -1, -1
    for i in range(H):
        for j in range(W):
            if not grid[i][j]:
                r, c = i, j
                break
        if r != -1: break
    
    if r == -1: return True

    tried_this_slot = set()
    for i in range(len(remaining_shapes)):
        shape_idx = remaining_shapes[i]
        if shape_idx in tried_this_slot:
            continue
        tried_this_slot.add(shape_idx)

        for orient in all_presents[shape_idx]:
            # Each orientation must cover the hole at (r, c)
            for dr, dc in orient:
                start_r, start_c = r - dr, c - dc
                if can_place(grid, orient, start_r, start_c, W, H):
                    place(grid, orient, start_r, start_c, 1)
                    if can_fit(grid, remaining_shapes[:i] + remaining_shapes[i+1:], all_presents, W, H):
                        return True
                    place(grid, orient, start_r, start_c, 0)
    return False

def main():

    with open('input.txt', 'r') as f:
        content = f.read()

    # Split the file into shapes and regions
    # We look for the first occurrence of "x" which denotes a region line
    parts = re.split(r'(\d+x\d+:)', content, maxsplit=1)
    if len(parts) < 2:
        print("Error: Could not split file into shapes and regions.")
        return
        
    shapes_section = parts[0]
    
    # Parse Shapes
    all_presents = {}
    # Find all "digit:" headers
    shape_matches = re.finditer(r'(\d+):', shapes_section)
    matches = list(shape_matches)
    
    for i, match in enumerate(matches):
        idx = int(match.group(1))
        start = match.end()
        # End is the start of the next match or the end of the section
        end = matches[i+1].start() if i+1 < len(matches) else len(shapes_section)
        
        shape_rows = shapes_section[start:end].strip().split('\n')
        coords = []
        for r, row in enumerate(shape_rows):
            for c, char in enumerate(row.strip()):
                if char == '#':
                    coords.append((r, c))
        if coords:
            all_presents[idx] = get_rotations_and_flips(coords)

    # Add Dummy shape for empty spaces
    all_presents[-1] = [[(0, 0)]]

    # Reconstruct the regions list
    region_lines = []
    for line in content.splitlines():
        if re.match(r'^\d+x\d+:', line):
            region_lines.append(line.strip())
    
    possible_count = 0
    for line in region_lines:
        header, counts = line.split(':')
        W, H = map(int, header.split('x'))
        quantities = list(map(int, counts.strip().split()))
        
        target_shapes = []
        total_area = 0
        for p_idx, qty in enumerate(quantities):
            if qty > 0:
                if p_idx not in all_presents:
                    continue
                shape_area = len(all_presents[p_idx][0])
                total_area += qty * shape_area
                for _ in range(qty):
                    target_shapes.append(p_idx)

        if total_area > (W * H) or not target_shapes:
            if total_area == 0 and not target_shapes: pass
            elif total_area > (W * H): pass
            else: pass
        else:
            # Add dummies for slack
            slack = (W * H) - total_area
            for _ in range(slack):
                target_shapes.append(-1)
            
            target_shapes.sort(key=lambda x: len(all_presents[x][0]), reverse=True)
            grid = [[0 for _ in range(W)] for _ in range(H)]
            if can_fit(grid, target_shapes, all_presents, W, H):
                possible_count += 1

    print(f"Total possible regions: {possible_count}")

if __name__ == "__main__":
    main()