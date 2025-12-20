# Summary

I confess I had to use Gemini for this one. :(

I initially tried to use `nx.all_simple_paths` but it didn't work for the large amount of input data we had. Gemini gave me this answer:


    We initialize a dictionary path_counts where "S" starts with 1 path.
    We use nx.topological_sort(G) to visit nodes in the correct dependency order (parents before children).
    For each node, we add its path count to all its successors.
    Finally, the count at node "X" gives the total number of paths from "S" to "X".