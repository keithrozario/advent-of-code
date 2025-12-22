import math
from typing import List
import networkx as nx


def get_distances(boxes: List[list])->List[dict]:
    """
    returns the distances between all pairs of boxes in the list.
    Distances are returned in sorted from nearest to furthest.
    """

    box_coords = []
    for box in boxes:
        coords = tuple(int(point) for point in box)
        box_coords.append(coords)

    distances = []
    for index, box_1 in enumerate(box_coords):
        for box_2 in box_coords[index+1:]:
            distances.append({
                "src": box_1,
                "dst": box_2,
                "dist": math.dist(box_2, box_1)
            })
    
    return sorted(distances, key=lambda x: x['dist'])


def get_wall_distance(boxes: list) -> int:
    """
    Connects the junction boxes till they form a full circuit (nx.is_connected)
    """

    distances = get_distances(boxes)
    wall_distance = 0
    G = nx.Graph()

    for box in boxes:
        # we construct a graph with all boxes first,
        # this ensures that we're not trying to checking for connected-ness on a graph with only some of the boxes
        G.add_node(tuple(int(point) for point in box))
    
    # continue till completion
    for distance in distances:
        if not nx.has_path(G,distance['src'],distance['dst']):
            G.add_edge(distance['src'],distance['dst'])

        if nx.is_connected(G):
            wall_distance = distance['src'][0] * distance['dst'][0]
            break
            
    return wall_distance

if __name__ == "__main__":

    with open("./2025/08/sample.txt", "r") as sample_file:
        boxes = [(line.strip().split(",")) for line in sample_file.readlines()]
    assert(get_distances(boxes)[0]['src']) == (162, 817, 812)
    assert(get_distances(boxes)[0]['dst']) == (425, 690, 689)
    assert(get_distances(boxes)[1]['dst']) == (431, 825, 988)
    print(get_wall_distance(boxes))


    with open("./2025/08/input.txt", "r") as boxes_file:
        boxes = [(line.strip().split(",")) for line in boxes_file.readlines()]
    print(get_wall_distance(boxes))