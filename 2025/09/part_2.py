from typing import List, Tuple

def get_area(tile_1: Tuple, tile_2: Tuple) -> int:
    x_length = abs(tile_1[0] - tile_2[0]) + 1
    y_length = abs(tile_1[1] - tile_2[1]) + 1
    return x_length * y_length

def is_point_in_polygon(x: float, y: float, polygon_points: List[Tuple]) -> bool:
    """
    Ray Casting algorithm to check if a point is inside the polygon.
    """
    n = len(polygon_points)
    inside = False
    for i in range(n):
        p1x, p1y = polygon_points[i]
        p2x, p2y = polygon_points[(i + 1) % n]
        
        # Check if the point is within the y-range of the edge
        if min(p1y, p2y) < y <= max(p1y, p2y):
            # Calculate the x-coordinate where the edge meets the ray's y
            if p1y != p2y:
                x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if x <= x_inters:
                    inside = not inside
    return inside

def is_vertex_inside(rect_p1: Tuple, rect_p2: Tuple, polygon_points: List[Tuple]) -> bool:
    x_min, x_max = sorted([rect_p1[0], rect_p2[0]])
    y_min, y_max = sorted([rect_p1[1], rect_p2[1]])
    
    for px, py in polygon_points:
        if x_min < px < x_max and y_min < py < y_max:
            return True 
    return False

def get_rectangle_sizes(red_tile_points: List[Tuple]) -> List[dict]:
    rectangles = []
    for index, tile_1 in enumerate(red_tile_points):
        for tile_2 in red_tile_points[index+1:]:
            rectangles.append({
                "src": tile_1,
                "dst": tile_2,
                "area": get_area(tile_1, tile_2)
            })
    return sorted(rectangles, key=lambda x: x['area'], reverse=True)

def does_edge_cross_rect(p1, p2, polygon_points):
    x_min, x_max = sorted([p1[0], p2[0]])
    y_min, y_max = sorted([p1[1], p2[1]])
    
    n = len(polygon_points)
    for i in range(n):
        e1 = polygon_points[i]
        e2 = polygon_points[(i + 1) % n]
        
        # Sort edge coordinates for range checking
        ex_min, ex_max = sorted([e1[0], e2[0]])
        ey_min, ey_max = sorted([e1[1], e2[1]])
        
        # If it's a vertical polygon edge
        if ex_min == ex_max:
            # Does the edge's X fall strictly inside the rectangle's X range?
            if x_min < ex_min < x_max:
                # Does the edge's Y range overlap the rectangle's Y range?
                if not (ey_max <= y_min or ey_min >= y_max):
                    return True
        
        # If it's a horizontal polygon edge
        elif ey_min == ey_max:
            # Does the edge's Y fall strictly inside the rectangle's Y range?
            if y_min < ey_min < y_max:
                # Does the edge's X range overlap the rectangle's X range?
                if not (ex_max <= x_min or ex_min >= x_max):
                    return True
                    
    return False

if __name__ == "__main__":
    # Standardize input reading
    with open("./2025/09/input.txt", "r") as sample_file:
        red_tiles = [line.strip() for line in sample_file if line.strip()]

    red_tile_points = [
        tuple(int(point) for point in tile.split(",")) for tile in red_tiles
    ]

    # 1. Get all candidate rectangles sorted by area
    all_rects = get_rectangle_sizes(red_tile_points)

    # 2. Iterate and find the first valid one
    largest_valid_area = 0
    for rect in all_rects:
        p1 = rect["src"]
        p2 = rect["dst"]
        
        # Calculate mathematical center
        cx = (p1[0] + p2[0]) / 2
        cy = (p1[1] + p2[1]) / 2

        # CHECK 1: Is center inside the polygon?
        if not is_point_in_polygon(cx, cy, red_tile_points):
            continue
            
        # CHECK 2: Does the polygon have a "poking" vertex inside our rectangle?
        if is_vertex_inside(p1, p2, red_tile_points):
            continue

        if does_edge_cross_rect(p1, p2, red_tile_points):
            continue
            
        # If it passes both, it's the largest!
        largest_valid_area = rect["area"]
        print(f"Largest valid rectangle found between {p1} and {p2}")
        print(f"Area: {largest_valid_area}")
        break