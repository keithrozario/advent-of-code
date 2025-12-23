import networkx as nx

def _count_paths_dp(G: nx.DiGraph, source_node: str, target_node: str) -> int:
    """Counts simple paths in a DAG from source to target using dynamic programming."""
    if source_node not in G.nodes() or target_node not in G.nodes():
        return 0 # Source or target not in graph, no paths

    path_counts = {node: 0 for node in G.nodes()}
    path_counts[source_node] = 1
    topological_order = list(nx.topological_sort(G))

    for u in topological_order:
        if path_counts[u] > 0: # Only propagate counts from reachable nodes
            for v in G.successors(u):
                path_counts[v] += path_counts[u]

    return path_counts.get(target_node, 0)

def calculate_paths(lines: list)->int:
    G = nx.DiGraph()

    for line in lines:
        src_raw, dst_raw = line.split(":")
        src = src_raw.strip()
        dst_machines = [machine.strip() for machine in dst_raw.strip().split(" ")]
        for dst_machine in dst_machines:
            if src and dst_machine:
                G.add_edge(src, dst_machine)

    source = "svr"
    target = "out"
    via_1 = "fft"
    via_2 = "dac"

    # Case 1: Path order is svr -> ... -> fft -> ... -> dac -> ... -> out
    paths_to_fft = _count_paths_dp(G, source, via_1)
    paths_fft_to_dac = _count_paths_dp(G, via_1, via_2)
    paths_dac_to_out = _count_paths_dp(G, via_2, target)
    total_order_1 = paths_to_fft * paths_fft_to_dac * paths_dac_to_out

    # Case 2: Path order is svr -> ... -> dac -> ... -> fft -> ... -> out
    paths_to_dac = _count_paths_dp(G, source, via_2)
    paths_dac_to_fft = _count_paths_dp(G, via_2, via_1)
    paths_fft_to_out = _count_paths_dp(G, via_1, target)
    total_order_2 = paths_to_dac * paths_dac_to_fft * paths_fft_to_out

    return total_order_1 + total_order_2


if __name__ == "__main__":
    with open("./2025/11/sample_2.txt", "r") as sample_file:
        lines = sample_file.readlines()

    print(calculate_paths(lines))

    with open("./2025/11/input.txt", "r") as input_file:
        lines = input_file.readlines()

    print(calculate_paths(lines))
