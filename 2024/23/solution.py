import networkx as nx

def get_input(file_name: str)->nx.Graph:
    with open(f"./23/{file_name}", "r") as f:
        lines = f.readlines()

    connections = []
    for line in lines:
        connections.append(tuple(line.strip().split("-")))
    
    G = nx.Graph()
    G.add_edges_from(connections)
    
    return G

def starts_with_letter(triangles: list[tuple[str,str,str]], letter: str='t')->int:
    
    triangle_starts_with_letter = 0
    
    for triangle in triangles:
        for node in triangle:
            if node.startswith("t"):
                triangle_starts_with_letter += 1
                break
    
    return triangle_starts_with_letter

def get_password(clique: list)->str:
    """
    Password = "sorted alphabetically, then joined together with commas"
    """
    clique.sort()
    password = ",".join(clique)
    return password

# Tests
G = get_input("sample.txt")
# part 1
triangles = [list(triangle) for triangle in nx.enumerate_all_cliques(G) if len(triangle) == 3]
assert len(triangles) == 12
starts_with_t = starts_with_letter(triangles=triangles, letter='t')
assert starts_with_t == 7
# part 2
## from docs: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.enumerate_all_cliques.html
## An iterator over cliques, each of which is a list of nodes in G. The cliques are ordered according to size.
cliques = [list(cliques) for cliques in nx.enumerate_all_cliques(G)]
max_clique_size = len(cliques[-1])
password = get_password(cliques[-1])
assert max_clique_size == 4
assert password == "co,de,ka,ta" 


# Part 1
G = get_input("input.txt")
cliques = [list(triangle) for triangle in nx.enumerate_all_cliques(G)]
triangles = [clique for clique in cliques if len(clique) == 3]
starts_with_t = starts_with_letter(triangles=triangles, letter='t')
print(f"There are {len(triangles)} in the graph")
print(f"There are {starts_with_t} triangles with a node starting with t")

# Part 2
max_clique_size = len(cliques[-1])
password = get_password(cliques[-1])
print(f"Max clique size: {max_clique_size}")
print(f"The Password is: {password}")
