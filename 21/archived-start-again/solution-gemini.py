import networkx as nx
from collections import deque
from itertools import product

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
    
    for r,c,target_index in product(range(4),range(3),range(len(target_code) + 1)):
      if (r,c) in layout:
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

def build_directional_graph(layout, moves, code):
    """Builds a graph representing the directional keypad navigation."""
    graph = nx.DiGraph()
    positions = {value: key for key, value in layout.items()}
    target_code = list(code)
    start_pos = positions['A']

    for r,c,target_index in product(range(2),range(3),range(len(target_code) + 1)):
        if (r,c) in layout:
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

def get_directional_keypad_layout():
    """Returns the directional keypad layout and position mapping."""
    layout = {
        (0, 1): '^', (0, 2): 'A',
        (1, 0): '<', (1, 1): 'v', (1, 2): '>'
    }
    positions = {value: key for key, value in layout.items()}
    return layout, positions

def find_shortest_sequences_graph(code, max_paths=500):
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
        path_count = 0
        for end in end_nodes:
            if path_count < max_paths:
                for path in nx.all_shortest_paths(graph, start_node, end):
                    if path_count < max_paths:
                        sequence = ""
                        for i in range(len(path) - 1):
                            move = graph[path[i]][path[i+1]]["move"]
                            sequence += move
                        if len(sequence) < min_length:
                            min_length = len(sequence)
                            shortest_sequences = [sequence]
                        elif len(sequence) == min_length:
                            shortest_sequences.append(sequence)
                        path_count+=1
                    else:
                        break
            else:
                break

    except nx.NetworkXNoPath:
        pass

    return sorted(shortest_sequences)

def find_shortest_directional_sequences_graph(code, max_paths=1000):
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
        path_count = 0
        for end in end_nodes:
            if path_count < max_paths:
                for path in nx.all_shortest_paths(graph, start_node, end):
                    if path_count < max_paths:
                        sequence = ""
                        for i in range(len(path) - 1):
                            move = graph[path[i]][path[i+1]]["move"]
                            sequence += move
                        if len(sequence) < min_length:
                            min_length = len(sequence)
                            shortest_sequences = [sequence]
                        elif len(sequence) == min_length:
                            shortest_sequences.append(sequence)
                        path_count += 1
                    else:
                        break
            else:
                break

    except nx.NetworkXNoPath:
        pass
    return sorted(shortest_sequences)

def get_final_sequence(door_code: str)->str:
    first_robot_sequence_prefix_cache = {}
    second_robot_sequence_prefix_cache = {}

    def find_shortest_directional_sequences_graph_with_cache(code):
        if code in second_robot_sequence_prefix_cache:
          return second_robot_sequence_prefix_cache[code]

        sequences = []

        for path_length in range(1,len(code)+1):
            sub_code = code[:path_length]
            if sub_code not in second_robot_sequence_prefix_cache:
              second_robot_sequence_prefix_cache[sub_code] = find_shortest_directional_sequences_graph(sub_code)

            sequences_for_sub_code = second_robot_sequence_prefix_cache[sub_code]
            
            if len(code) == path_length:
              sequences.extend(sequences_for_sub_code)

            
        second_robot_sequence_prefix_cache[code] = sequences
        return sequences


    def find_shortest_sequences_graph_with_cache(code):
        if code in first_robot_sequence_prefix_cache:
          return first_robot_sequence_prefix_cache[code]
        
        sequences = []
        for path_length in range(1, len(code)+1):
            sub_code = code[:path_length]
            if sub_code not in first_robot_sequence_prefix_cache:
              first_robot_sequence_prefix_cache[sub_code] = find_shortest_sequences_graph(sub_code)
            
            sequences_for_sub_code = first_robot_sequence_prefix_cache[sub_code]
            if len(code) == path_length:
                sequences.extend(sequences_for_sub_code)

        first_robot_sequence_prefix_cache[code] = sequences
        return sequences

    first_robot_sequences = find_shortest_sequences_graph_with_cache(door_code)
    
    second_robot_sequences = []
    for sequence in first_robot_sequences:
        second_robot_sequences.extend(find_shortest_directional_sequences_graph_with_cache(sequence))
    
    my_sequences = []
    for sequence in second_robot_sequences:
        my_sequences.extend(find_shortest_directional_sequences_graph_with_cache(sequence))
    
    if my_sequences:
        shortest_sequence = min(my_sequences, key=len)
    else:
        return ""

    return shortest_sequence

# Test cases
# door_code = "980A"
# shortest_sequence = get_final_sequence(door_code)
# print(f"{door_code}: {shortest_sequence}")
# assert shortest_sequence == "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A<"

door_code = "179A"
shortest_sequence = get_final_sequence(door_code)
print(f"{door_code}: {shortest_sequence}")
assert len(shortest_sequence) == len("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

door_code = "456A"
shortest_sequence = get_final_sequence(door_code)
print(f"{door_code}: {shortest_sequence}")
assert shortest_sequence == "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"

door_code = "379A"
shortest_sequence = get_final_sequence(door_code)
print(f"{door_code}: {shortest_sequence}")
assert shortest_sequence == "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"
