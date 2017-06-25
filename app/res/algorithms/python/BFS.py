import random
import sys

import time


def bfs2(graph, start):
    visited = set()
    visited.add(start)
    queue = [start]
    c = 0
    dr = 0
    while dr < len(queue):
        c += 1
        vertex = queue[dr]
        dr += 1
        for i in graph[vertex]:
            if i not in visited:
                visited.add(i)
                queue.append(i)


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
bfs2(g, 1)
end = int(round(time.time() * 1000))
print(end-start)

