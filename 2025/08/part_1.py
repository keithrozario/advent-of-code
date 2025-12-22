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


def construct_graph(boxes: list) -> nx.Graph:

    num_boxes_to_connect = 1000
    distances = get_distances(boxes)
    G = nx.Graph()
    for i, distance in enumerate(distances[:num_boxes_to_connect]):
        # connect the two boxes
        G.add_edge(distance['src'],distance['dst'])
    
    return G

if __name__ == "__main__":

    with open("./2025/08/sample.txt", "r") as sample_file:
        boxes = [(line.strip().split(",")) for line in sample_file.readlines()]
    assert(get_distances(boxes)[0]['src']) == (162, 817, 812)
    assert(get_distances(boxes)[0]['dst']) == (425, 690, 689)
    assert(get_distances(boxes)[1]['dst']) == (431,825,988)

    with open("./2025/08/input.txt", "r") as boxes_file:
        boxes = [(line.strip().split(",")) for line in boxes_file.readlines()]

    boxes_graph = construct_graph(boxes)
    lengths  = [len(c) for c in sorted(nx.connected_components(boxes_graph), key=len, reverse=True)]
    total = 1 
    for length in lengths[:3]:
        total *= length
    print(total)