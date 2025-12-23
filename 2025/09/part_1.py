from typing import List, Tuple

def get_area(tile_1: Tuple, tile_2: Tuple)->int:

    x_length = abs(tile_1[0] - tile_2[0]) + 1
    y_length = abs(tile_1[1] - tile_2[1]) + 1

    return x_length * y_length

def get_rectangle_sizes(red_tiles: List[str])->List[dict]:
    """
    returns the size of rectangles between all pairs of red_tiles
    Rectangles are returned in a dict, and sorted biggest to smallest
    """

    red_tile_points = [
        tuple(int(point) for point in tile.split(",")) for tile in red_tiles
    ]

    rectangles = []
    for index, tile_1 in enumerate(red_tile_points):
        for tile_2 in red_tile_points[index+1:]:
            rectangles.append({
                "src": tile_1,
                "dst": tile_2,
                "area": get_area(tile_1,tile_2)
            })
    
    return sorted(rectangles, key=lambda x: x['area'], reverse=True)


if __name__ == "__main__":
    with open("./2025/09/sample.txt", "r") as sample_file:
        red_tiles = sample_file.readlines()

    rectangles = get_rectangle_sizes(red_tiles=red_tiles)
    print(rectangles[0]['area'])

    with open("./2025/09/input.txt", "r") as input_file:
        red_tiles = input_file.readlines()

    rectangles = get_rectangle_sizes(red_tiles=red_tiles)
    print(rectangles[0]['area'])


