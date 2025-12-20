from typing import List
import networkx as nx

def calculate_splits(map: List[list])->int:
    G = nx.DiGraph()

    for row, line in enumerate(map):
        for col, cell in enumerate(line):
            if map[row][col] == "S":

                map[row+1][col] = "|"
                G.add_edge("S", (row+1,col))
            
            elif cell == "^":
                if map[row-1][col] == "|":
                    map[row][col+1] = "|"
                    G.add_edge( (row-1,col), (row,col+1))
                    
                    map[row][col-1] = "|"
                    G.add_edge( (row-1,col), (row,col-1))

            elif map[row-1][col] == '|':
                map[row][col] = "|"
                G.add_edge( (row-1,col), (row,col))
    
    for column, cell in enumerate(map[-1]):
        if cell == "|":
            G.add_edge((len(map)-1,column),"X")

    # Use dynamic programming to count paths since the graph is a DAG.
    path_counts = {node: 0 for node in G.nodes()}
    path_counts["S"] = 1
    for node in nx.topological_sort(G):
        if path_counts[node] > 0:
            for successor in G.successors(node):
                path_counts[successor] += path_counts[node]
    number_of_paths = path_counts.get("X", 0)
    return number_of_paths


if __name__ == "__main__":
    with open("./2025/07/super_simple_sample.txt", 'r') as sample_file:
        map = [list(line.strip()) for line in sample_file.readlines()]

    assert calculate_splits(map) == 4

    with open("./2025/07/sample.txt", 'r') as sample_file:
        map = [list(line.strip()) for line in sample_file.readlines()]

    assert calculate_splits(map) == 40

    with open("./2025/07/input.txt", 'r') as input_file:
        map = [list(line.strip()) for line in input_file.readlines()]
    
    total_splits = calculate_splits(map)
    print(total_splits)
