import networkx as nx
from itertools import product

def build_keypad_graph_with_moves():
    """Builds a graph representing the numeric keypad, with edges labeled by moves."""
    graph = nx.DiGraph()  # Use a directed graph to represent moves

    # Define keypad layout and positions
    layout = {
        (0, 0): '7', (0, 1): '8', (0, 2): '9',
        (1, 0): '4', (1, 1): '5', (1, 2): '6',
        (2, 0): '1', (2, 1): '2', (2, 2): '3',
        (3, 1): '0', (3, 2): 'A'
    }

    # Add nodes to the graph
    for row, col in layout:
        graph.add_node(layout[(row, col)])

    # Define possible moves (up, down, left, right)
    moves = {
        'up': (-1, 0, '^'),  # (row change, col change, move label)
        'down': (1, 0, 'v'),
        'left': (0, -1, '<'),
        'right': (0, 1, '>')
    }

    # Add edges based on valid moves with move labels
    for (row, col), value in layout.items():
        for move_name, (dr, dc, move_label) in moves.items():
            next_row, next_col = row + dr, col + dc
            if (next_row, next_col) in layout:
                graph.add_edge(value, layout[(next_row, next_col)], move=move_label)

    return graph

def build_directional_keypad_graph_with_moves():
    """Builds a graph representing the numeric keypad, with edges labeled by moves."""
    graph = nx.DiGraph()  # Use a directed graph to represent moves

    # Define keypad layout and positions
    layout = {
        (0, 1): '^', (0, 2): 'A',
        (1, 0): '<', (1, 1): 'v', (1, 2): '>',
    }

    # Add nodes to the graph
    for row, col in layout:
        graph.add_node(layout[(row, col)])

    # Define possible moves (up, down, left, right)
    moves = {
        'up': (-1, 0, '^'),  # (row change, col change, move label)
        'down': (1, 0, 'v'),
        'left': (0, -1, '<'),
        'right': (0, 1, '>')
    }

    # Add edges based on valid moves with move labels
    for (row, col), value in layout.items():
        for move_name, (dr, dc, move_label) in moves.items():
            next_row, next_col = row + dr, col + dc
            if (next_row, next_col) in layout:
                graph.add_edge(value, layout[(next_row, next_col)], move=move_label)

    return graph

def get_path_moves(graph, paths):
    """Gets the sequence of moves for the shortest path between two keys."""

    moves = []
    for path in paths:
        path_move = ""
        for i in range(len(path) - 1):
            path_move += graph[path[i]][path[i+1]]['move']
        moves.append(path_move)
    return moves


def generate_all_paths(path_dict):
    sorted_steps = sorted(path_dict.keys())
    possible_moves_per_step = [path_dict[step] for step in sorted_steps]
    all_combinations = product(*possible_moves_per_step)
    all_paths = ["A".join(combination)+"A" for combination in all_combinations]

    return all_paths

def get_dict_all_pairs_shortest_paths(G: nx.graph):
    """
    Dict of shortest path is the dictionary of shortest paths where the key is 2-D, [FROM][TO]
    and the value is a list of paths that are the shorted distance between the two keys in arrow format
    """
    all_shortest_paths = nx.all_pairs_all_shortest_paths(G)
    dict_of_shortest_paths = {}
    for num_path in all_shortest_paths:
        num_from = num_path[0]
        dict_of_shortest_paths[num_from] = {}
        for num_to in num_path[1].keys():
            dict_of_shortest_paths[num_from][num_to] = get_path_moves(G, num_path[1][num_to])
      
    return dict_of_shortest_paths


def calc_distance(code: str, dict_of_shortest_paths: dict) -> int:
    distance = 0
    for i, char in enumerate(code[:-1]):
        distance += len(dict_of_shortest_paths[char][code[i+1]])

    return distance

def get_shortest_key_moves(code_list: list, dict_of_shortest_paths: dict):
    
    output_paths = []
    min_distance = 0

    for code in code_list:
        full_code = 'A' + code
        directional_keypad_moves = {}
        for i, char in enumerate(full_code[:-1]):
            directional_keypad_moves[i] = dict_of_shortest_paths[full_code[i]][full_code[i+1]]
        temp_paths = generate_all_paths(directional_keypad_moves)
        output_paths.extend(temp_paths)
    
     
    min_len = len(min(output_paths, key=len))
    same_length_outputs = [output for output in output_paths if len(output) == min_len]

    if '<' in dict_of_shortest_paths.keys():
        final_output = []
        for output in same_length_outputs:
            distance = calc_distance(output, dict_of_shortest_paths)
            if distance <= min_distance or min_distance == 0:
                min_distance = distance
                final_output.append(output)
        return final_output
    else:
        return same_length_outputs


def get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional, rounds: int=2):
    output = get_shortest_key_moves([code], dict_of_shortest_paths)

    for round in range(rounds):
        print(f"Round: {round}")
        output = get_shortest_key_moves(output, dict_of_shortest_paths_directional)

    return output

def calculate_complexity(keypad_code, final_sequence):
    
    numeric_code = int(keypad_code.replace('A', ''))
    complexity = numeric_code * len(final_sequence[0])  

    return complexity

directional_keypad_graph = build_directional_keypad_graph_with_moves()
dict_of_shortest_paths_directional = get_dict_all_pairs_shortest_paths(directional_keypad_graph)
keypad_graph = build_keypad_graph_with_moves()
dict_of_shortest_paths = get_dict_all_pairs_shortest_paths(keypad_graph)



# ## Tests
# complexities = 0
# code = '029A'
# output = get_shortest_key_moves([code], dict_of_shortest_paths)
# # assert '<A^A^^>AvvvA' in output
# output_directional = get_shortest_key_moves(output, dict_of_shortest_paths_directional)
# # assert 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A' in output_directional
# final_sequence = get_shortest_key_moves(output_directional, dict_of_shortest_paths_directional)
# # assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' in final_sequence
       
# assert calculate_complexity(code, final_sequence) == (68 * 29)
# complexities += calculate_complexity(code, final_sequence)

# code = '980A'
# final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional)
# complexities += calculate_complexity(code, final_sequence)
# # assert '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A' in final_sequence

# code = '179A'
# final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional)
# complexities += calculate_complexity(code, final_sequence)
# # assert '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A' in final_sequence

# code = '456A'
# final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional)
# complexities += calculate_complexity(code, final_sequence)
# # assert '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A' in final_sequence

# code = '379A'
# final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional)
# complexities += calculate_complexity(code, final_sequence)
# # assert '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A' in final_sequence

# assert complexities == 126384

# Part 1
# with open('./21/input.txt', 'r') as f:
#     door_codes = f.readlines()
#     complexities = 0
#     for code in door_codes:
#         code = code.strip()
#         final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional)
#         complexities += calculate_complexity(code, final_sequence)
#     print(f"Part 1: {complexities}")

# Part 2
with open('./21/input.txt', 'r') as f:
    door_codes = f.readlines()
    complexities = 0
    for code in door_codes:
        code = code.strip()
        print("Starting sequence calculation")
        final_sequence = get_final_sequence(code, dict_of_shortest_paths, dict_of_shortest_paths_directional, 5)
        print("Complete")
        complexities += calculate_complexity(code, final_sequence)
    print(f"Part 1: {complexities}")


"""
"<A" ==> v<<A>>^A
"v<<A" ==> <vA<AA>>^A
">>^A" ==> AA<^A>A
"""