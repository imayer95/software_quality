import random
import sys

import time


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(set(graph[vertex]) - visited)
    return visited


def create_random_tree(n):
    a = list(range(2, n))
    b = [1]

    g = {}
    r = random.randint(1, n-1)
    g = {1: [r]}
    for i in range(2, n):
        t = random.randint(1, i-1)
        r = random.randint(i, n)

        x = a.pop(r-i-1)
        b.append(x)
        t -= 1
        if b[t] not in g.keys():
            g[b[t]] = list()
        if x not in g.keys():
            g[x] = list()
        g[b[t]].append(x)
        g[x].append(b[t])

    return g

nodes = int(sys.argv[1])

g = create_random_tree(nodes)
start = int(round(time.time() * 1000))
dfs(g, 1)
end = int(round(time.time() * 1000))
print(end-start)

