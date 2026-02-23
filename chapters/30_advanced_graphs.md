# Chapter 30: Advanced Graph Algorithms

> *"Bridges, articulation points, strong components, and max flow — the heavy machinery of graphs."*

---

## 30.1 Why These Topics Matter

**Chapter 8** covered BFS/DFS and **Chapter 21** covered Dijkstra, MST, and topological sort. Here we go deeper: **bridges** and **articulation points** (critical edges and vertices whose removal increases connected components), **strongly connected components (SCC)** in full detail, and **max flow / min cut**. These appear in advanced interviews, competitive programming, and systems (e.g. network reliability, bipartite matching). Mastery signals expert-level graph fluency.

---

## 30.2 Bridges (Cut Edges)

A **bridge** is an edge whose removal increases the number of connected components.

**Idea:** Use DFS. For each edge (u, v), if there is **no back edge** from the subtree of v to u or an ancestor of u, then (u, v) is a bridge. We track **discovery time** and **low link**: `low[u]` = minimum discovery time reachable from u by following tree edges and at most one back edge.

**Formula:** Run DFS; for each node u, set:
- `disc[u]` = discovery time
- `low[u]` = min of: disc[u], disc[w] for every back edge (u,w), and low[child] for every tree child.

**Edge (parent, u) is a bridge** iff `low[u] > disc[parent]` (no back edge from u's subtree to parent or above).

```python
def find_bridges(graph, n):
    """graph: adjacency list, n = number of vertices. Returns list of (u,v) bridges."""
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    bridges = []
    timer = [0]

    def dfs(u):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if disc[v] == -1:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    return bridges
```

**Time:** O(V + E).

---

## 30.3 Articulation Points (Cut Vertices)

A vertex is an **articulation point** if its removal increases the number of connected components.

**Idea:** In the DFS tree, root is AP if it has more than one child. For non-root u, u is AP if it has a child v such that **low[v] ≥ disc[u]** — no back edge from v's subtree to above u.

```python
def find_articulation_points(graph, n):
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    ap = [False] * n
    timer = [0]

    def dfs(u):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in graph[u]:
            if disc[v] == -1:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    return [i for i in range(n) if ap[i]]
```

**Time:** O(V + E).

---

## 30.4 Strongly Connected Components (SCC)

A **strongly connected component** is a maximal set of vertices such that every pair has a path in both directions. Used in directed graphs.

**Kosaraju's algorithm:** (1) DFS and push nodes to stack by **finish time**. (2) Reverse all edges. (3) Pop from stack and DFS on the reversed graph; each DFS tree is one SCC.

**Tarjan's algorithm:** One DFS. Each node gets `disc` and `low`; use a stack and "on stack" flag. When `low[u] == disc[u]`, u is the root of an SCC; pop stack until u and that's one SCC.

```python
def tarjan_scc(graph, n):
    disc = [-1] * n
    low = [-1] * n
    on_stack = [False] * n
    stack = []
    sccs = []
    timer = [0]

    def dfs(u):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        stack.append(u)
        on_stack[u] = True
        for v in graph[u]:
            if disc[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], disc[v])
        if low[u] == disc[u]:
            comp = []
            while True:
                v = stack.pop()
                on_stack[v] = False
                comp.append(v)
                if v == u:
                    break
            sccs.append(comp)

    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    return sccs
```

**Time:** O(V + E).

---

## 30.5 Max Flow (Conceptual)

**Problem:** Directed graph with **capacities** on edges. Source s, sink t. Find the maximum amount of "flow" from s to t (flow ≤ capacity on each edge; flow conserved at internal nodes).

**Ford-Fulkerson:** Repeatedly find an **augmenting path** (path with residual capacity) and push flow along it. With **integer** capacities, total flow is bounded; with BFS for the path we get **Edmonds-Karp**: O(V E²).

**Min-cut:** Max flow value = capacity of a **minimum s-t cut** (set of edges whose removal disconnects s from t). Finding the cut: after max flow, the set of nodes reachable from s in the **residual graph** defines one side of the min cut.

**Applications:** Bipartite matching (max matching = max flow in a constructed graph), project selection, etc.

---

## 30.6 Complexity Summary

| Problem | Algorithm | Time |
|---------|-----------|------|
| Bridges | DFS + low/disc | O(V + E) |
| Articulation points | DFS + low/disc | O(V + E) |
| SCC | Tarjan or Kosaraju | O(V + E) |
| Max flow | Edmonds-Karp | O(V E²) |

---

## Practice Exercises

**E1.** Count the number of bridges in an undirected graph. (Use the bridge-finding DFS above.)

**E2.** After computing SCCs, how do you build the **condensation graph** (DAG of SCCs)? (Each SCC becomes one node; edge from SCC A to B if there was an edge from some node in A to some node in B.)

**E3.** (Conceptual) How is **bipartite maximum matching** reduced to max flow? (Source connected to left part, sink to right part; edges from left to right; capacities 1.)

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Bridge | Edge (u,v) with low[v] > disc[u]; DFS with low/disc |
| Articulation point | Vertex whose removal disconnects; root: 2+ children; else low[child] ≥ disc[u] |
| SCC | Tarjan: one DFS, stack, low = disc → pop SCC |
| Max flow | Augmenting paths; min-cut = max-flow value |

**Previous:** [Chapter 29 → Suffix Array & Suffix Tree](29_suffix_array_tree.md) | **Next:** [Chapter 31 → Advanced DP](31_advanced_dp.md)
