# Chapter 8: Graphs

> *"Graphs are just 'nodes and edges.' The rest is representation and traversal."*

---

## 8.1 Why Graphs Matter

Graphs model relationships: social networks, maps, dependencies, grids. Interview problems often present as **matrix grids** (adjacent cells = edges), **lists of edges**, or **adjacency lists**. The core skills are: (1) choosing a representation, (2) **BFS** for shortest path in unweighted graphs and level-by-level exploration, (3) **DFS** for cycles, connected components, and topological order. Weighted shortest paths (Dijkstra, Bellman-Ford) and MST are in **Chapter 21**. Here we focus on fundamentals so you never get stuck on "how do I even traverse this graph?"

---

## 8.2 Terminology

| Term | Meaning |
|------|---------|
| **Vertex (node)** | Entity; we often use 0..n-1 as IDs |
| **Edge** | Connection between two vertices; (u, v) or (u, v, weight) |
| **Directed** | Edge has direction (u → v) |
| **Undirected** | Edge goes both ways; model as two directed edges |
| **Weighted** | Each edge has a cost; unweighted = unit cost |
| **Degree** | Undirected: number of edges. Directed: in-degree, out-degree |
| **Path** | Sequence of vertices connected by edges |
| **Cycle** | Path that starts and ends at the same vertex |
| **Connected** | Undirected: there is a path between every pair |
| **Strongly connected** | Directed: there is a path from every u to every v |

---

## 8.3 Representations

### Example graph (undirected)

```
    0 --- 1
    | \   |
    |  \  |
    2 --- 3
         /
        4
```

Vertices: 0, 1, 2, 3, 4. Edges: (0,1), (0,2), (0,3), (1,3), (2,3), (3,4).

### Adjacency list (preferred for interviews)

For each vertex, store a list (or set) of neighbors. For weighted: list of (neighbor, weight).

**Adjacency list for the example graph above:**
- 0 → [1, 2, 3]
- 1 → [0, 3]
- 2 → [0, 3]
- 3 → [0, 1, 2, 4]
- 4 → [3]

```python
# Unweighted: list of lists
n = 5   # vertices 0..4
graph = [[] for _ in range(n)]
# Add edge u -> v
def add_edge(u, v):
    graph[u].append(v)
# Undirected: add both
def add_undirected(u, v):
    graph[u].append(v)
    graph[v].append(u)

# Weighted: list of (neighbor, weight)
graph_w = [[] for _ in range(n)]
def add_weighted(u, v, w):
    graph_w[u].append((v, w))
```

**Space:** O(V + E). **Iterate neighbors of u:** O(degree(u)).

### Adjacency matrix

`adj[i][j]` = 1 if edge (i,j) exists (or weight). Good for dense graphs and "is there an edge?" in O(1).

```python
# Unweighted
adj = [[0] * n for _ in range(n)]
adj[u][v] = 1

# Weighted
adj[u][v] = weight
```

**Space:** O(V²). **Iterate neighbors of u:** O(V).

### Edge list

List of (u, v) or (u, v, w). Useful for Kruskal (sort edges) and when building the graph from input.

```python
edges = [(0, 1), (1, 2), (2, 0)]
```

---

## 8.4 Breadth-First Search (BFS)

Explore in **layers**: start from a node (distance 0), then all nodes at distance 1, then distance 2, etc. Use a **queue**: process a node, then add its unvisited neighbors to the back. BFS from a source gives **shortest path lengths** (in number of edges) in an **unweighted** graph.

**BFS order from node 0** (same graph as above):

```
    0 --- 1      Layer 0: 0
    | \   |      Layer 1: 1, 2, 3  (neighbors of 0)
    2 --- 3      Layer 2: 4        (neighbor of 3, 1 and 2 already visited)
         /
        4

Queue: [0] → pop 0, add 1,2,3 → [1,2,3] → pop 1, add nothing new → pop 2, add nothing → pop 3, add 4 → [4] → pop 4.
Distances: dist[0]=0, dist[1]=1, dist[2]=1, dist[3]=1, dist[4]=2.
```

```python
from collections import deque

def bfs(graph, start):
    """graph: adjacency list (list of lists). Returns distances from start."""
    n = len(graph)
    dist = [-1] * n
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**Time:** O(V + E). **Space:** O(V).

To **reconstruct a shortest path**, keep a parent array: when you set `dist[v] = dist[u] + 1`, set `parent[v] = u`. Then walk back from target to start.

---

## 8.5 Multisource BFS

You have **multiple starting nodes** (e.g., all cells with value 0). Initialize the queue with all of them at distance 0; run BFS as usual. Every node gets the distance to the **nearest** source.

```python
def multisource_bfs(graph, sources):
    n = len(graph)
    dist = [-1] * n
    q = deque()
    for s in sources:
        dist[s] = 0
        q.append(s)
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**0/1 BFS:** When edge weights are only 0 or 1, shortest path can be done with a **deque**: push at front if edge weight 0, at back if weight 1. Same idea as Dijkstra but O(V + E). (Details in **Chapter 21**.)

---

## 8.6 Depth-First Search (DFS)

Go deep first: from a node, recurse (or use a stack) on one neighbor, then the next. Use for **cycle detection**, **connected components**, **topological sort**, and exploring all reachable nodes.

**Recursive:**

```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    # process start here
    for v in graph[start]:
        if v not in visited:
            dfs_recursive(graph, v, visited)
    return visited
```

**Iterative (stack):**

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        # process u here
        for v in graph[u]:
            if v not in visited:
                stack.append(v)
    return visited
```

**Time:** O(V + E). **Space:** O(V) for visited; O(h) for recursion stack where h is max depth.

---

## 8.7 Connected Components (Undirected)

Run DFS (or BFS) from an unvisited node; mark all reachable nodes. Repeat from the next unvisited node. Each run is one component.

```python
def count_components(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = [False] * n
    count = 0
    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
    for i in range(n):
        if not visited[i]:
            count += 1
            dfs(i)
    return count
```

---

## 8.8 Cycle Detection

- **Undirected:** DFS; if you see an edge to an already-visited node, it's a cycle — but ignore the "parent" (the node you came from). So: (u, v) is a back edge iff v is visited and v ≠ parent[u].
- **Directed:** DFS with a **current path** set. If you reach a node that's in the current path, there's a cycle. When leaving a node, remove it from the path. (Or use three colors: white/gray/black; gray = in current path.)

```python
def has_cycle_directed(graph):
    n = len(graph)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def dfs(u):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False
    return any(color[i] == WHITE and dfs(i) for i in range(n))
```

---

## 8.9 Topological Sort (Directed Acyclic Graph)

A **topological order** is a linear ordering of vertices such that for every edge (u, v), u comes before v. Only exists for **DAGs** (no cycle).

**DFS approach:** Do DFS, and **append a node to the result when we finish (postorder)**. Reverse the result. Finishing times decrease along any path, so reversing gives a valid order.

```python
def topological_sort_dfs(graph):
    n = len(graph)
    visited = [False] * n
    order = []
    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        order.append(u)
    for i in range(n):
        if not visited[i]:
            dfs(i)
    return order[::-1]
```

**Kahn's algorithm (BFS):** Compute in-degrees. Enqueue all with in-degree 0. Dequeue u, append to order, decrease in-degree of neighbors; enqueue any that become 0. If final order length ≠ n, there is a cycle. See **Chapter 21** for more.

---

## 8.10 Grid as Graph

A 2D grid is a graph: each cell is a node; edges to 4 or 8 neighbors. Common pattern:

```python
def grid_neighbors(grid, r, c, four=True):
    R, C = len(grid), len(grid[0])
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    if not four:
        dr += [-1, -1, 1, 1]
        dc += [-1, 1, -1, 1]
    for i in range(len(dr)):
        nr, nc = r + dr[i], c + dc[i]
        if 0 <= nr < R and 0 <= nc < C:
            yield nr, nc
```

Then run BFS/DFS on (row, col) as node id, or use (r * C + c) as integer id.

---

## 8.11 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| BFS / DFS (full graph) | O(V + E) | O(V) |
| Build adjacency list | O(V + E) | O(V + E) |
| Connected components | O(V + E) | O(V) |
| Topological sort (DFS) | O(V + E) | O(V) |

---

## 8.12 When to Use BFS vs DFS

- **Shortest path (unweighted)** → BFS.
- **Explore all reachable nodes** → BFS or DFS; BFS gives levels.
- **Cycle detection** → DFS (with parent or current-path set).
- **Connected components** → DFS or BFS.
- **Topological order** → DFS (postorder + reverse) or Kahn's BFS.
- **Path existence / count paths** → DFS with backtracking.

---

## Practice Exercises

### Easy

**E1.** Number of Islands — 2D grid of '1' and '0'; count connected components of '1's. DFS or BFS per component.

**E2.** Flood Fill — from (sr, sc) replace color with new color in connected region. BFS/DFS.

**E3.** Find if path exists in graph (undirected) — DFS/BFS from start to target.

### Medium

**E4.** Clone Graph — copy a graph (node with neighbors). BFS/DFS + map old node → new node.

**E5.** Course Schedule — can you finish all courses (edges = prerequisites)? Topological sort or cycle detection.

**E6.** Number of Connected Components in Undirected Graph — build graph from edges, count components.

**E7.** Shortest Path in Binary Matrix — unweighted grid; BFS from (0,0) to (n-1,n-1).

### Hard

**E8.** Word Ladder — BFS in implicit graph (words differing by one letter).

**E9.** Critical Connections in a Network — find bridges (edges whose removal increases components). DFS with discovery time and low link.

---

## Chapter Summary

| Technique | Use Case |
|-----------|----------|
| BFS | Shortest path (unweighted), levels |
| Multisource BFS | Multiple sources, nearest source |
| DFS | Components, cycles, topological order |
| Adjacency list | Default representation |
| Grid → graph | 4/8 neighbors, (r,c) or r*C+c |

**Previous:** [Chapter 7 → Heaps](07_heaps.md) | **Next:** [Chapter 9 → Tries](09_tries.md)
