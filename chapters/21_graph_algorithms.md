# Chapter 21: Graph Algorithms

> *"Shortest path and minimum spanning tree are the two pillars of graph algorithms. Know when to use which."*

---

## 21.1 Why Graph Algorithms Matter

**Chapter 8** covered graph representation, BFS, and DFS. Here we add **weighted shortest path** (Dijkstra, Bellman-Ford), **all-pairs** (Floyd-Warshall), **minimum spanning tree** (Prim, Kruskal), **topological sort** (Kahn, DFS), and **strongly connected components**. These appear in interviews as "shortest path", "cheapest flight", "network delay", "critical connections", or "course schedule". Heaps (Chapter 7) and Union-Find (Chapter 10) are used by Dijkstra and Kruskal.

---

## 21.2 Dijkstra's Algorithm (Single-Source Shortest Path, Non-Negative Weights)

**Idea:** Greedily expand the closest unvisited node; update distances to neighbors. When all weights are non-negative, the first time we pop a node, we have its shortest distance. Use a **min-heap** (priority, node).

```python
import heapq

def dijkstra(n, graph, start):
    # graph: list of list of (neighbor, weight)
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

**Time:** O((V + E) log V) with binary heap. **Space:** O(V).

---

## 21.3 Bellman-Ford (Negative Weights, Cycle Detection)

Relax all edges V-1 times. If a V-th pass still relaxes an edge, there is a negative cycle reachable from source. Single-source distances are correct only when no negative cycle.

```python
def bellman_ford(n, edges, start):
    # edges: list of (u, v, weight)
    dist = [float('inf')] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Optional: detect negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # negative cycle
    return dist
```

**Time:** O(V × E).

---

## 21.4 Floyd-Warshall (All-Pairs Shortest Path)

dp[k][i][j] = shortest path from i to j using only vertices 0..k. Simplify to 2D: for k in range(n): for i, j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]). Initialize dist[i][j] = 0 if i==j, weight(i,j) if edge, else inf.

```python
def floyd_warshall(n, edges):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
```

**Time:** O(V³). **Use when:** Dense graph, all-pairs, or negative weights (no negative cycle).

---

## 21.5 Minimum Spanning Tree (MST)

**MST** = spanning tree with minimum total edge weight. Two classic algorithms:

### Kruskal's Algorithm

Sort edges by weight; add edge if it doesn't form a cycle (Union-Find). See **Chapter 10**.

```python
def kruskal(n, edges):
    uf = UnionFind(n)
    edges.sort(key=lambda e: e[2])
    mst_weight = 0
    for u, v, w in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += w
    return mst_weight
```

**Time:** O(E log E) for sort; Union-Find nearly O(1) per op.

### Prim's Algorithm

Start from a vertex; repeatedly add the minimum-weight edge that connects the current tree to a new vertex. Use a **min-heap** of (weight, v) where v is outside the tree; when popping v, add v to tree and push all edges from v.

**Time:** O(E log V) with heap.

---

## 21.6 Topological Sort (DAG)

**Kahn's algorithm (BFS):** In-degrees; queue all with in-degree 0; dequeue, append to order, reduce neighbors' in-degree; enqueue if 0. If final order length ≠ n, there is a cycle.

```python
def topological_sort_kahn(n, graph):
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None  # None if cycle
```

**DFS:** Postorder (append when finishing); reverse the list. See **Chapter 8**.

---

## 21.7 Strongly Connected Components (SCC)

**Kosaraju's algorithm (brief):** (1) DFS, record finish times. (2) Reverse all edges. (3) DFS in decreasing order of finish time; each DFS tree is one SCC. **Tarjan's** uses one DFS with low-link values. For interviews, knowing "SCC = maximal set of mutually reachable nodes" and that Kosaraju/Tarjan exist is often enough.

---

## 21.8 Bidirectional BFS

For **unweighted** shortest path, you can run BFS from both source and target. Alternate one level from each side; when the two frontiers meet, you have the distance. Cuts the explored space in half for large graphs. Use when the graph is huge and one-way BFS would explore too many nodes.

---

## 21.9 A* Search (Conceptual)

**A*** is best-first search with a heuristic h(v) = estimated cost from v to goal. Priority = g(v) + h(v) where g(v) = cost from start. When h is **admissible** (never overestimates), A* finds an optimal path. Used in pathfinding and puzzles. Implementation: like Dijkstra but with priority = distance + h(node). For interviews, knowing "Dijkstra + heuristic" is usually enough.

---

## 21.10 Complexity Summary

| Algorithm | Time | Use Case |
|-----------|------|----------|
| Dijkstra | O((V+E) log V) | Single-source, non-negative weights |
| Bellman-Ford | O(VE) | Negative weights, cycle detection |
| Floyd-Warshall | O(V³) | All-pairs |
| Kruskal | O(E log E) | MST |
| Prim | O(E log V) | MST |
| Topological (Kahn) | O(V+E) | DAG order |

---

## Practice Exercises

**E1.** Network Delay Time — Dijkstra from source; answer = max of distances (or -1 if any inf).

**E2.** Cheapest Flights Within K Stops — BFS with at most K+1 layers, or Bellman-Ford K+1 iterations.

**E3.** Course Schedule I/II — topological sort / Kahn; detect cycle.

**E4.** Min Cost to Connect All Points — MST (Kruskal or Prim); edges = all pairs with Manhattan distance.

**E5.** Critical Connections — bridges (edges not in any cycle); Tarjan or DFS with discovery time and low link.

**E6.** Word Ladder (unweighted) — BFS; bidirectional BFS for optimization.

---

## Chapter Summary

| Need | Algorithm |
|------|-----------|
| Shortest path (non-negative) | Dijkstra |
| Negative weights / cycle | Bellman-Ford |
| All-pairs | Floyd-Warshall |
| MST | Kruskal (UF) or Prim (heap) |
| Order in DAG | Topological (Kahn or DFS) |
| Unweighted shortest (large) | Bidirectional BFS |

**Previous:** [Chapter 20 → Divide & Conquer](20_divide_and_conquer.md) | **Next:** [Chapter 22 → String Algorithms](22_string_algorithms.md)
