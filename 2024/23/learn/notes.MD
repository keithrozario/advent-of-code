Using `networkx` really saved me time here.

After a tiny bit of refactoring, I got part 2, down to just one line of code:

```python
    cliques = [list(triangle) for triangle in nx.enumerate_all_cliques(G)]
    max_clique_size = len(cliques[-1])
```

This would not have been possible had I used a custom solution. But because the package saved me time, whenever I encounter these interesting problems (e.g. 2-D Arrays, or Graphs) I should use the packages that already have all this functionality written and battle-tested, rather than crafting my own.
