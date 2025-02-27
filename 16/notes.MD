This was a tough one. The LLMs helped me a lot with part 1, but set me on the wrong path with part 2.

Part was super easy, and I had to learn heaps (who knew!) in Python. This was an interesting solution the problem, albeit with some superfluous code (literally a function that was written but never used).

Part 2 was much much harder, eventually I solved it with a lot of elbow grease and understanding.

Glad I completed this.

The last piece about deduplication is also useful. Gemini recommended I write a whole bespoke function to deduplicate a list of list

```

def deduplicate_list_of_lists(list_of_lists):
    """
    Deduplicates a list of lists, ensuring each unique sublist appears only once.

    Args:
        list_of_lists: A list where each element is another list (e.g., [[1, 2], [3, 4], [1, 2]]).

    Returns:
        A new list of lists with duplicates removed. The order of the first appearance of unique lists
        is preserved.
    """
    seen = set()
    result = []
    for sublist in list_of_lists:
        # Convert the sublist to a tuple because lists are unhashable and cannot be put in a set
        sublist_tuple = tuple(sublist)
        if sublist_tuple not in seen:
            seen.add(sublist_tuple)
            result.append(sublist)
    return result


```

While [this](https://stackoverflow.com/questions/2213923/removing-duplicates-from-a-list-of-lists) post from stackoverflow reduces the amount of code to a more manageable 2 lines using the built-in itertools.
```
>>> k = [[1, 2], [4], [5, 6, 2], [1, 2], [3], [4]]
>>> import itertools
>>> k.sort()
>>> list(k for k,_ in itertools.groupby(k))
[[1, 2], [3], [4], [5, 6, 2]]

```