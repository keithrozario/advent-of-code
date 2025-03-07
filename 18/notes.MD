Wow, great puzzle.

I re-used question 16's heap search to find the answer. Spent abour 3 hours debugging a simple issue (I had mixed up the x and y axis). But the mode worked, and worked OK even for part 2 with minimum tweaking. However, part 2 was a bit slow ... kinda like 12 seconds to run. So I decided to loop through in a binary fashion, I asked Gemini to generate me some code to do that -- and it gave me something else.

When I prompted it to use a in-built python library instead ... it didn't give me a better binary search, but asked me to use networkx instead.

Networkx was amazing. ONce I had a grid of the maze, it creates a graph to show which points are reachable from which other points. And then with a single line, solves the puzzle!!!!

    path = nx.shortest_path(graph, start, end)

Bloody...fucking...hell!!

It's amazing. One solution that is so simple and maintainable.

THen I prompted it for a better binary search (again!) and this  time it worked. And now the solution runs in under 1 second (including tests)