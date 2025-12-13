import networkx as nx
from collections import deque

def get_keypad_layout():
    """Returns the numeric keypad layout and position mapping."""
    layout = {
        (0, 0): '7', (0, 1): '8', (0, 2): '9',
        (1, 0): '4', (1, 1): '5', (1, 2): '6',
        (2, 0): '1', (2, 1): '2', (2, 2): '3',
        (3, 1): '0', (3, 2): 'A'
    }
    positions = {value: key for key, value in layout.items()}
    return layout, positions

def get_directional_keypad_moves():
    """Returns the directional keypad moves and their effects."""
    moves = {
        '^': (-1, 0),  # Up
        'v': (1, 0),   # Down
        '<': (0, -1),  # Left
        '>': (0, 1),   # Right
        'A': (0, 0)  # activate on current numpad
    }
    return moves

def is_valid_move(row, col, layout):
    """Checks if a move is within the numeric keypad bounds."""
    return (row, col) in layout

def build_graph(layout, moves, code):
    """Builds a graph representing the keypad navigation."""
    graph = nx.DiGraph()
    positions = {value: key for key, value in layout.items()}
    target_code = list(code)
    start_pos = positions['A']
    
    for r in range(4):
        for c in range(3):
            if (r,c) in layout:
                for target_index in range(len(target_code) + 1):
                    
                    current_state = ((r,c),target_index)
                    
                    for move, (dr, dc) in moves.items():
                        if move == 'A':
                            if target_index < len(target_code) and layout.get((r,c)) == target_code[target_index]:
                                next_state = ((r,c), target_index + 1)
                                graph.add_edge(current_state, next_state, move=move)

                        else:
                            next_r, next_c = r + dr, c + dc
                            if is_valid_move(next_r, next_c, layout):
                                next_state = ((next_r, next_c), target_index)
                                graph.add_edge(current_state, next_state, move=move)

    return graph, ((start_pos[0], start_pos[1]), 0), (0,0)


def find_shortest_sequences_graph(code):
    """Finds the shortest sequences using a graph representation."""
    layout, _ = get_keypad_layout()
    moves = get_directional_keypad_moves()
    graph, start_node, end_node  = build_graph(layout, moves, code)
    target_code = list(code)
    end_nodes = []

    for node in graph.nodes:
        if node[1] == len(target_code):
            end_nodes.append(node)

    shortest_sequences = []
    min_length = float('inf')
    
    
    try:
        for end in end_nodes:
            paths = nx.all_shortest_paths(graph, start_node, end)

            for path in paths:
                sequence = ""
                for i in range(len(path) - 1):
                    
                    move = graph[path[i]][path[i+1]]["move"]
                    sequence += move
                if len(sequence) < min_length:
                        min_length = len(sequence)
                        shortest_sequences = [sequence]
                elif len(sequence) == min_length:
                        shortest_sequences.append(sequence)

    except nx.NetworkXNoPath:
        pass

    return sorted(shortest_sequences)

def get_directional_keypad_layout():
    """Returns the directional keypad layout and position mapping."""
    layout = {
        (0, 1): '^', (0, 2): 'A',
        (1, 0): '<', (1, 1): 'v', (1, 2): '>'
    }
    positions = {value: key for key, value in layout.items()}
    return layout, positions

def build_directional_graph(layout, moves, code):
    """Builds a graph representing the directional keypad navigation."""
    graph = nx.DiGraph()
    positions = {value: key for key, value in layout.items()}
    target_code = list(code)
    start_pos = positions['A']

    for r in range(2):
        for c in range(3):
            if (r,c) in layout:
                for target_index in range(len(target_code) + 1):
                    current_state = ((r,c), target_index)

                    for move, (dr,dc) in moves.items():

                        if move == 'A':
                            if target_index < len(target_code) and layout.get((r,c)) == target_code[target_index]:
                                next_state = ((r,c), target_index + 1)
                                graph.add_edge(current_state, next_state, move = move)
                        else:
                            next_r, next_c = r + dr, c + dc

                            if is_valid_move(next_r, next_c, layout):
                                next_state = ((next_r, next_c), target_index)
                                graph.add_edge(current_state, next_state, move = move)

    return graph, ((start_pos[0],start_pos[1]), 0)

def find_shortest_directional_sequences_graph(code):
    """Finds the shortest sequences for a directional keypad."""
    layout, _ = get_directional_keypad_layout()
    moves = get_directional_keypad_moves()
    graph, start_node = build_directional_graph(layout, moves, code)
    target_code = list(code)
    end_nodes = []

    for node in graph.nodes:
        if node[1] == len(target_code):
            end_nodes.append(node)

    shortest_sequences = []
    min_length = float('inf')
    
    try:
        for end in end_nodes:
            paths = nx.all_shortest_paths(graph, start_node, end)
            for path in paths:
                sequence = ""
                for i in range(len(path) - 1):
                    move = graph[path[i]][path[i+1]]["move"]
                    sequence += move

                if len(sequence) < min_length:
                    min_length = len(sequence)
                    shortest_sequences = [sequence]
                elif len(sequence) == min_length:
                    shortest_sequences.append(sequence)
    except nx.NetworkXNoPath:
        pass
    return sorted(shortest_sequences)

def get_final_sequence(door_code: str)->str:

    first_robot_sequences = find_shortest_sequences_graph(door_code)
    
    second_robot_sequences = []
    for sequence in first_robot_sequences:
        second_robot_sequences.extend(find_shortest_directional_sequences_graph(sequence))
    
    my_sequences = []
    for sequence in second_robot_sequences:
        my_sequences.extend(find_shortest_directional_sequences_graph(sequence))
    
    shortest_sequence = min(my_sequences, key=len)

    return shortest_sequence

# Test cases for second directional keypad
# door_code = "029A"
# first_robot_sequences = find_shortest_sequences_graph(door_code)
# print(f"First robot sequences for door code {door_code}: {first_robot_sequences}")
# assert len(first_robot_sequences) == 3
# assert "<A^A>^^AvvvA" in first_robot_sequences
# assert "<A^A^^>AvvvA" in first_robot_sequences
# # 2nd Robot
# second_robot_sequences = find_shortest_directional_sequences_graph("<A^A>^^AvvvA")
# assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in second_robot_sequences
# # my sequence
# my_sequences = find_shortest_directional_sequences_graph("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
# assert "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A" in my_sequences

# door_code = "980A"
# shortest_sequence = get_final_sequence(door_code)
# print(f"{door_code}: {shortest_sequence}")
# assert len(shortest_sequence) == len("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A")

# door_code = "179A"
# shortest_sequence = get_final_sequence(door_code)
# print(f"{door_code}: {shortest_sequence}")
# assert len(shortest_sequence) == len("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

# door_code = "456A"
# shortest_sequence = get_final_sequence(door_code)
# print(f"{door_code}: {shortest_sequence}")
# assert shortest_sequence == "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"

door_code = "379A"
shortest_sequence = get_final_sequence(door_code)
print(f"{door_code}: {shortest_sequence}")
assert shortest_sequence == "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"