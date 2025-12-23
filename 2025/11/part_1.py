import networkx as nx

def calculate_paths(lines: list)->int:
    G = nx.DiGraph()

    for line in lines:
        src, dst = line.split(":")
        dst_machines = [machine for machine in dst.strip().split(" ")]
        for dst_machine in dst_machines:
            G.add_edge(src, dst_machine)

    paths = nx.all_simple_paths(G, source="you", target="out")
    number_of_paths = sum(1 for path in paths)

    return number_of_paths


if __name__ == "__main__":
    with open("./2025/11/sample.txt", "r") as sample_file:
        lines = sample_file.readlines()

    print(calculate_paths(lines))

    with open("./2025/11/input.txt", "r") as input_file:
        lines = input_file.readlines()

    print(calculate_paths(lines))
