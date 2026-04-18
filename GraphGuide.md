# Graph Algorithms

---

## TABLE OF CONTENTS
1. [BFS — Breadth-First Search](#1-bfs--breadth-first-search)
2. [DFS — Depth-First Search](#2-dfs--depth-first-search)
3. [Dijkstra's Algorithm](#3-dijkstras-algorithm)
4. [A* Algorithm](#4-a-algorithm)
5. [Topological Sort](#5-topological-sort)
6. [Cycle Detection](#6-cycle-detection)
7. [Union-Find (Disjoint Set Union)](#7-union-find-disjoint-set-union)

---

## 1. BFS — Breadth-First Search

### Theory
BFS explores a graph **level by level**, starting from a source node. It uses a **queue (FIFO)** to process nodes in the order they were discovered. It guarantees the **shortest path in terms of number of edges** (unweighted graphs).

Key properties:
- Visits all nodes at distance `k` before visiting nodes at distance `k+1`
- Ideal for: shortest path (unweighted), level-order traversal, multi-source BFS, connected components
- Works on both directed and undirected graphs

### Algorithm

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()          # Process front of queue
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Enqueue unvisited neighbors

    return order
```

**Shortest path variant:**
```python
def bfs_shortest_path(graph, start, end):
    visited = {start: None}  # node -> parent
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == end:
            # Reconstruct path
            path = []
            while node is not None:
                path.append(node)
                node = visited[node]
            return path[::-1]

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)

    return []  # No path found
```

### Complexity
| | Value |
|---|---|
| **Time** | O(V + E) — every vertex and edge visited once |
| **Space** | O(V) — queue + visited set |

### Step-by-Step Example

**Graph:**
```
    A
   / \
  B   C
 / \   \
D   E   F
```
Adjacency list: `{A:[B,C], B:[D,E], C:[F], D:[], E:[], F:[]}`

**BFS from A:**

| Step | Queue | Visited | Output |
|------|-------|---------|--------|
| Start | [A] | {A} | |
| Dequeue A, enqueue B,C | [B,C] | {A,B,C} | A |
| Dequeue B, enqueue D,E | [C,D,E] | {A,B,C,D,E} | A,B |
| Dequeue C, enqueue F | [D,E,F] | {A,B,C,D,E,F} | A,B,C |
| Dequeue D | [E,F] | same | A,B,C,D |
| Dequeue E | [F] | same | A,B,C,D,E |
| Dequeue F | [] | same | A,B,C,D,E,F |

**Result:** `[A, B, C, D, E, F]` — level by level ✓

**Shortest path from A to F:**
- Level 0: A
- Level 1: B, C
- Level 2: D, E, **F** ← found at distance 2
- Path: A → C → F

### Key Interview Patterns
- **Multi-source BFS**: Push all sources into the queue at start (e.g., "walls spreading", "rotten oranges")
- **0-1 BFS**: Use deque; push weight-0 edges to front, weight-1 edges to back
- **BFS on grid**: Treat each cell as a node, 4 or 8 directions as edges

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 🟡 Medium | Multi-source BFS — start all rotten oranges simultaneously |
| 2 | [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 🟡 Medium | BFS on grid, 8-directional movement |
| 3 | [542. 01 Matrix](https://leetcode.com/problems/01-matrix/) | 🟡 Medium | Multi-source BFS from all 0s to find distance to nearest 0 |
| 4 | [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | 🔴 Hard | BFS on implicit graph — fewest transformation steps |
| 5 | [1162. As Far from Land as Possible](https://leetcode.com/problems/as-far-from-land-as-possible/) | 🟡 Medium | Multi-source BFS from all land cells |
| 6 | [433. Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/) | 🟡 Medium | BFS shortest path — similar to Word Ladder, good warm-up |

> 💡 **Start with 994, then 1091.** These two cover multi-source BFS and grid BFS — the two patterns that appear most at senior level.

### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🎓 Abdul Bari | [Graph Traversals — BFS & DFS](https://www.youtube.com/watch?v=pcKY4hjDrxk) | Theory-first, very clear whiteboard explanation |
| 🟢 NeetCode | [DFS vs BFS — When to Use Which?](https://www.youtube.com/watch?v=cS-198wtfj0) | Interview decision-making perspective |
| 🟢 NeetCode | [Top 5 Graph Algorithms for Coding Interviews](https://www.youtube.com/watch?v=utDu3Q7Flrw) | All major graph patterns in one video |

---

## 2. DFS — Depth-First Search

### Theory
DFS explores a graph by going **as deep as possible** before backtracking. Uses a **stack** (explicit or via recursion call stack). 

Key properties:
- Explores one path completely before trying alternatives
- Ideal for: cycle detection, topological sort, connected components, path existence, solving mazes
- Works on both directed and undirected graphs

### Algorithm

**Recursive:**
```python
def dfs_recursive(graph, node, visited=None, order=None):
    if visited is None:
        visited = set()
        order = []

    visited.add(node)
    order.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)

    return order
```

**Iterative (explicit stack):**
```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()              # Process top of stack
        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        for neighbor in reversed(graph[node]):  # reversed to match recursive order
            if neighbor not in visited:
                stack.append(neighbor)

    return order
```

### Complexity
| | Value |
|---|---|
| **Time** | O(V + E) — every vertex and edge visited once |
| **Space** | O(V) — recursion stack / explicit stack + visited |

> ⚠️ Recursion depth can hit Python's default limit (~1000). Use iterative DFS or `sys.setrecursionlimit()` for large graphs.

### Step-by-Step Example

**Same graph as BFS:**
```
    A
   / \
  B   C
 / \   \
D   E   F
```

**DFS from A (recursive):**

```
Visit A → go to B
  Visit B → go to D
    Visit D → no unvisited neighbors → backtrack
  Visit E → no unvisited neighbors → backtrack
Back to A → go to C
  Visit C → go to F
    Visit F → no unvisited neighbors → backtrack
```

**Result:** `[A, B, D, E, C, F]` — deep dive, then backtrack ✓

### DFS Tree Edge Classification (crucial for senior interviews)
When running DFS on a **directed graph**, edges fall into 4 categories:

| Edge Type | Description | Use |
|-----------|-------------|-----|
| **Tree edge** | Edge used to discover a new node | Forms DFS tree |
| **Back edge** | Points to an ancestor in DFS tree | Indicates **cycle** in directed graph |
| **Forward edge** | Points to a descendant (non-tree) | Directed graphs only |
| **Cross edge** | Points to a node in different DFS subtree | Directed graphs only |

**Implementation with timestamps:**
```python
def dfs_classify(graph):
    color = {}   # WHITE=unvisited, GRAY=in-stack, BLACK=done
    has_cycle = [False]

    def dfs(u):
        color[u] = 'GRAY'
        for v in graph.get(u, []):
            if color.get(v) == 'GRAY':  # Back edge → cycle!
                has_cycle[0] = True
            elif color.get(v) != 'BLACK':
                dfs(v)
        color[u] = 'BLACK'

    for node in graph:
        if node not in color:
            dfs(node)

    return has_cycle[0]
```

### Key Interview Patterns
- **All paths** from source to target: DFS with backtracking
- **Island counting**: DFS to "flood fill" each connected region
- **Articulation points / bridges**: DFS with low-link values (Tarjan's)
- **Strongly Connected Components**: Kosaraju's or Tarjan's (DFS-based)

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | 🟡 Medium | DFS flood-fill — count disconnected components |
| 2 | [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | 🟡 Medium | DFS with return value accumulation |
| 3 | [417. Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | 🟡 Medium | Reverse DFS from both oceans — classic multi-source |
| 4 | [130. Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | 🟡 Medium | DFS from boundary — invert the problem thinking |
| 5 | [329. Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | 🔴 Hard | DFS + memoization on grid — tests depth-first + DP combo |
| 6 | [797. All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/) | 🟡 Medium | DFS backtracking — enumerate all paths in DAG |

> 💡 **Start with 200, then 417.** Number of Islands is the canonical DFS problem. Pacific Atlantic tests whether you can run DFS from multiple sources in reverse — a very senior-level thinking shift.

### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🎓 Abdul Bari | [Graph Traversals — BFS & DFS](https://www.youtube.com/watch?v=pcKY4hjDrxk) | Covers DFS theory with stack trace walkthrough |
| 🟢 NeetCode | [Graph Problems Playlist](https://www.youtube.com/playlist?list=PLot-Xpze53ldBT_7QA8NVot219jFNr_GI) | All DFS/BFS LeetCode solutions with explanation |
| 🎬 Jenny's Lectures | [BFS and DFS Graph Traversals](https://www.youtube.com/watch?v=vf-cxgUXcMk) | Step-by-step with adjacency matrix and list |

---

## 3. Dijkstra's Algorithm

### Theory
Dijkstra finds the **shortest path from a single source to all other nodes** in a graph with **non-negative edge weights**. It's a greedy algorithm that always processes the closest unvisited node next.

Core idea: **Relaxation** — if we find a shorter path to a node through a neighbor, update its distance.

Key properties:
- Only works with **non-negative weights** (use Bellman-Ford for negative weights)
- Greedy: once a node is finalized (popped from heap), its distance is optimal
- Used heavily in: maps/navigation, network routing, robot pathfinding

### Algorithm

```python
import heapq

def dijkstra(graph, start):
    """
    graph: dict of {node: [(neighbor, weight), ...]}
    Returns: dist dict with shortest distances from start
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}  # For path reconstruction

    # Min-heap: (distance, node)
    heap = [(0, start)]

    while heap:
        curr_dist, u = heapq.heappop(heap)

        # Skip if we already found a better path (stale entry)
        if curr_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:          # Relaxation step
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev

def reconstruct_path(prev, start, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    return path[::-1] if path[-1] == start else []
```

### Complexity
| | Binary Heap | Fibonacci Heap |
|---|---|---|
| **Time** | O((V + E) log V) | O(E + V log V) |
| **Space** | O(V) | O(V) |

> In practice, binary heap (Python's `heapq`) is standard. Fibonacci heap is theoretical.

### Step-by-Step Example

**Weighted graph:**
```
        2
   A -------> B
   |          |
 4 |        1 |
   |          |
   C -------> D
        3
   A -------> D (weight 10)
```

Graph:
```python
graph = {
    'A': [('B', 2), ('C', 4), ('D', 10)],
    'B': [('D', 1)],
    'C': [('D', 3)],
    'D': []
}
```

**Running Dijkstra from A:**

| Step | Heap (dist, node) | dist[A] | dist[B] | dist[C] | dist[D] |
|------|-------------------|---------|---------|---------|---------|
| Init | [(0,A)] | 0 | ∞ | ∞ | ∞ |
| Pop A | [(2,B),(4,C),(10,D)] | 0 | **2** | **4** | **10** |
| Pop B | [(3,D),(4,C),(10,D)] | 0 | 2 | 4 | **3** |
| Pop D(3) | [(4,C),(10,D)] | 0 | 2 | 4 | 3 |
| Pop C(4) | [(10,D)] | 0 | 2 | 4 | 3 (no update, 4+3=7 > 3) |
| Pop D(10) | [] | — | — | — | skip (stale) |

**Final shortest distances from A:** `{A:0, B:2, C:4, D:3}`
**Shortest path A→D:** A → B → D (cost 3) ✓

### Key Interview Patterns
- **Modified Dijkstra**: Change the cost function (e.g., minimize max edge, minimize number of hops)
- **K-th shortest path**: Use modified heap with state `(dist, node, k)`
- **Dijkstra on grid**: Nodes are cells, weights are terrain costs

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | 🟡 Medium | Classic Dijkstra — single source, find max of all shortest paths |
| 2 | [1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | 🟡 Medium | Modified Dijkstra on grid — minimize max difference along path |
| 3 | [787. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 🟡 Medium | Dijkstra with extra state `(cost, node, stops_remaining)` |
| 4 | [1514. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/) | 🟡 Medium | Max-heap Dijkstra — flip to maximization instead of minimization |
| 5 | [778. Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) | 🔴 Hard | Dijkstra where cost = max cell value along path |
| 6 | [1976. Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) | 🟡 Medium | Dijkstra + count paths of equal shortest distance |


### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🔵 William Fiset | [Dijkstra's Shortest Path — Graph Theory](https://www.youtube.com/watch?v=pSqmAO-m7Lk) | Deep theory + implementation, best for conceptual understanding |
| 🎓 Abdul Bari | [Dijkstra Algorithm — Greedy Method](https://www.youtube.com/watch?v=XB4MIexjvY0) | Classic whiteboard walkthrough with worked example |
| 🎯 CS Dojo / Interview Prep | [Dijkstra's Algorithm for Coding Interviews](https://www.youtube.com/watch?v=pLElbKBc4RU) | Interview-focused, covers heap implementation |

---

## 4. A* Algorithm

### Theory
A* is an **informed search algorithm** — an extension of Dijkstra that uses a **heuristic function** to guide the search toward the goal. Instead of blindly exploring all directions, it prioritizes nodes that seem closer to the destination.

**Key formula:**
```
f(n) = g(n) + h(n)
```
- `g(n)` = actual cost from start to node `n` (same as Dijkstra's `dist`)
- `h(n)` = **heuristic** estimate of cost from `n` to goal
- `f(n)` = total estimated cost of path through `n`

**Admissible heuristic**: `h(n)` must never **overestimate** the true cost. This guarantees optimality.

Common heuristics:
| Heuristic | Formula | Use Case |
|-----------|---------|----------|
| **Manhattan distance** | `|x1-x2| + |y1-y2|` | Grid with 4-directional movement |
| **Euclidean distance** | `√((x1-x2)² + (y1-y2)²)` | Grid with diagonal movement |
| **Chebyshev distance** | `max(|x1-x2|, |y1-y2|)` | 8-directional movement |
| **Zero heuristic** | `h(n) = 0` | Degenerates to Dijkstra |

### Algorithm

```python
import heapq

def astar(grid, start, goal):
    """
    grid: 2D list (0=free, 1=wall)
    start, goal: (row, col) tuples
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

    # Heap: (f_score, g_score, node)
    open_set = [(heuristic(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        # Skip stale entries
        if g > g_score.get(current, float('inf')):
            continue

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:  # 4 directions
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g_score[current] + 1  # cost to move = 1

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return []  # No path
```

### Complexity
| | Value |
|---|---|
| **Time** | O(E log V) — depends heavily on heuristic quality |
| **Space** | O(V) |

> With a perfect heuristic, A* explores only the optimal path. With h=0, it's identical to Dijkstra.

### Step-by-Step Example

**5×5 grid (0=free, 1=wall), S=start, G=goal:**
```
S . . 1 .
. 1 . 1 .
. 1 . . .
. . . 1 G
. . . 1 .
```
Start = (0,0), Goal = (3,4)

**A* explores:**

| Explored | g | h (Manhattan to G) | f |
|----------|---|---------------------|---|
| (0,0) | 0 | 7 | 7 |
| (1,0) | 1 | 6 | 7 |
| (2,0) | 2 | 5 | 7 |
| (3,0) | 3 | 4 | 7 |
| (3,1) | 4 | 3 | 7 |
| (3,2) | 5 | 2 | 7 |
| (2,2) | 4 | 3 | 7 |
| (2,3) | 5 | 2 | 7 |
| (2,4) | 6 | 1 | 7 |
| (3,4) | 7 | 0 | 7 ✓ |

A* consistently followed the path with f=7, never wasting time on dead ends!

**Path found:** (0,0)→(1,0)→(2,0)→(2,2)→(2,3)→(2,4)→(3,4)

### A* vs Dijkstra
| | Dijkstra | A* |
|---|---|---|
| Strategy | Explores all directions equally | Guided toward goal |
| Heuristic | None (h=0) | Domain-specific |
| Optimal? | Always | Yes, if h is admissible |
| Speed | Slower on large graphs | Much faster in practice |
| Best for | All-pairs shortest path | Single target pathfinding |

### Key Interview Patterns
- **Weighted A\***: Multiply heuristic by factor > 1 for faster (suboptimal) paths
- **Bidirectional A\***: Run A* from both ends, meet in the middle

### Practice Problems

> ⚠️ LeetCode doesn't have explicit "use A*" problems — but these are the ones where A* is the intended optimal approach and knowing it will impress interviewers.

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 🟡 Medium | BFS works, but A* with Chebyshev distance is faster — great to mention in interview |
| 2 | [1293. Shortest Path in a Grid with Obstacles Elimination](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/) | 🔴 Hard | BFS with state `(row, col, k_remaining)` — A* heuristic dramatically reduces search |
| 3 | [675. Cut Off Trees for Golf Event](https://leetcode.com/problems/cut-off-trees-for-golf-event/) | 🔴 Hard | BFS between multiple targets sequentially — A* optimizes each leg |
| 4 | [2290. Minimum Obstacle Removal to Reach Corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/) | 🔴 Hard | 0-1 BFS or Dijkstra on grid — same family as A* on weighted grids |

> 💡 For A*, the interview value is explaining the heuristic choice and why it's admissible. Even if you code BFS/Dijkstra, saying "I'd optimize this with A* using Manhattan distance as the heuristic" is a strong senior signal.

### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🖥️ Computerphile | [A\* Search Algorithm](https://www.youtube.com/watch?v=ySN5Wnu88nE) | Best conceptual intro — concise, visual, explains f=g+h clearly |
| 🎮 Sebastian Lague | [A\* Pathfinding E01: Algorithm Explanation](https://www.youtube.com/watch?v=-L-WgKMFuhE) | Visual grid walkthrough — directly mirrors warehouse robot navigation |
| 🎮 Sebastian Lague | [A\* Pathfinding Full Series (Playlist)](https://www.youtube.com/playlist?list=PLFt_AvWsXl0cq5Umv3pMC9SPnKjfp9eGW) | Deep dive: heap optimization, path smoothing, threading |


---

## 5. Topological Sort

### Theory
Topological sort produces a **linear ordering of vertices** in a **Directed Acyclic Graph (DAG)** such that for every directed edge `u → v`, vertex `u` comes before `v` in the ordering.

Key properties:
- Only valid for **DAGs** (no cycles)
- A graph may have **multiple valid** topological orderings
- Ideal for: task scheduling, dependency resolution, build systems, course prerequisites

### Two Approaches

---

### Approach 1: Kahn's Algorithm (BFS-based)

**Idea:** Repeatedly remove nodes with **in-degree 0** (no dependencies).

```python
from collections import deque

def topological_sort_kahn(graph, num_nodes):
    """
    graph: dict {node: [neighbors]}
    Returns topological order, or [] if cycle exists
    """
    in_degree = {i: 0 for i in range(num_nodes)}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    # Start with all nodes that have no incoming edges
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If order doesn't contain all nodes → cycle exists
    return order if len(order) == num_nodes else []
```

---

### Approach 2: DFS-based

**Idea:** Run DFS; after fully exploring a node (all descendants visited), push it to a stack. Reverse the stack for the final order.

```python
def topological_sort_dfs(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)   # Push AFTER all descendants are done

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]  # Reverse for correct order
```

### Complexity
| | Value |
|---|---|
| **Time** | O(V + E) |
| **Space** | O(V) |

### Step-by-Step Example

**Course prerequisites (classic problem):**
```
Course 0 requires: none
Course 1 requires: 0
Course 2 requires: 0
Course 3 requires: 1, 2
Course 4 requires: 3
```
Graph: `{0:[1,2], 1:[3], 2:[3], 3:[4], 4:[]}`

**Kahn's Algorithm:**

Initial in-degrees: `{0:0, 1:1, 2:1, 3:2, 4:1}`

| Step | Queue | Process | Updated in-degrees | Order |
|------|-------|---------|-------------------|-------|
| 1 | [0] | 0 | 1→0, 2→0 | [0] |
| 2 | [1,2] | 1 | 3→1 | [0,1] |
| 3 | [2] | 2 | 3→0 | [0,1,2] |
| 4 | [3] | 3 | 4→0 | [0,1,2,3] |
| 5 | [4] | 4 | — | [0,1,2,3,4] |

**Result:** `[0, 1, 2, 3, 4]` — valid course order ✓

### Key Interview Patterns
- **Detect cycle in directed graph**: Kahn's — if output length < V, cycle exists
- **Alien Dictionary (LeetCode 269)**: Build graph from character ordering, then topo sort
- **Parallel scheduling**: Group nodes by levels (BFS-style topo sort gives layers)

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | 🟡 Medium | Topo sort / cycle detection — can you complete all courses? |
| 2 | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 🟡 Medium | Return actual topological order (Kahn's algorithm) |
| 3 | [269. Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | 🔴 Hard | Build DAG from sorted word list → topo sort (⚠️ Premium) |
| 4 | [2115. Find All Possible Recipes from Given Supplies](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/) | 🟡 Medium | Topo sort with starting nodes (ingredients = initial supply) |
| 5 | [310. Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | 🟡 Medium | Reverse topo sort — peel leaves inward to find roots |
| 6 | [1857. Largest Color Value in a Directed Graph](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/) | 🔴 Hard | Topo sort + DP tracking color counts — tests both skills together |


### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🔵 William Fiset | [Topological Sort \| Kahn's Algorithm \| Graph Theory](https://www.youtube.com/watch?v=cIBFEhD77b4) | Clean theory explanation with source code |
| 🎯 Striver (TakeUForward) | [Detect Cycle in Directed Graph using Topo Sort (BFS)](https://www.youtube.com/watch?v=iTBaI90lpDQ) | Interview-style, shows how topo sort doubles as cycle detection |
| 🟢 NeetCode | [Course Schedule II — Topological Sort](https://www.youtube.com/watch?v=Akt3glAwyfY) | Direct LeetCode 210 walkthrough |

---

## 6. Cycle Detection

### Theory
Cycle detection checks if a graph contains a cycle — a path that starts and ends at the same node.

The approach differs for directed vs undirected graphs:

| | Directed Graph | Undirected Graph |
|---|---|---|
| Method | DFS with 3-color marking | DFS with parent tracking / Union-Find |
| Key insight | Back edge = cycle | Re-visiting a node ≠ cycle (check parent) |

---

### Directed Graph — DFS with Colors

```python
def has_cycle_directed(graph):
    """
    Colors: 0=WHITE (unvisited), 1=GRAY (in current DFS path), 2=BLACK (fully explored)
    """
    color = {}

    def dfs(node):
        color[node] = 1  # GRAY — currently exploring

        for neighbor in graph.get(node, []):
            if color.get(neighbor, 0) == 1:  # Back edge! Found cycle
                return True
            if color.get(neighbor, 0) == 0:  # WHITE — not yet visited
                if dfs(neighbor):
                    return True

        color[node] = 2  # BLACK — done
        return False

    for node in graph:
        if color.get(node, 0) == 0:
            if dfs(node):
                return True

    return False
```

---

### Undirected Graph — DFS with Parent Tracking

```python
def has_cycle_undirected(graph):
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Visited but not parent → cycle
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True

    return False
```

### Complexity
| | Value |
|---|---|
| **Time** | O(V + E) |
| **Space** | O(V) — recursion stack |

### Step-by-Step Example

**Directed Graph:**
```
A → B → C → D
        ↑   |
        └───┘
```
Graph: `{A:[B], B:[C], C:[D], D:[C]}`  ← D→C creates cycle

**DFS Trace:**
```
dfs(A) → color[A]=GRAY
  dfs(B) → color[B]=GRAY
    dfs(C) → color[C]=GRAY
      dfs(D) → color[D]=GRAY
        neighbor C → color[C]==GRAY → CYCLE FOUND! ✓
```

**Undirected Graph:**
```
A — B — C
    |   |
    D ——+   ← B-D-C forms a cycle
```
Graph: `{A:[B], B:[A,C,D], C:[B,D], D:[B,C]}`

**DFS Trace from A:**
```
dfs(A, parent=-1) → visit A
  dfs(B, parent=A) → visit B
    dfs(C, parent=B) → visit C
      dfs(D, parent=C) → visit D
        neighbor B: visited, B != parent(C)? Yes → CYCLE FOUND! ✓
```

### Key Interview Patterns
- **LeetCode 207 (Course Schedule)**: Directed cycle detection = impossible schedule
- **LeetCode 684 (Redundant Connection)**: Undirected cycle via Union-Find
- **Negative cycle detection**: Use Bellman-Ford (can't use DFS)

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | 🟡 Medium | Directed cycle — 3-color DFS or Kahn's |
| 2 | [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | 🟡 Medium | Undirected cycle — Union-Find: find the edge that closes a cycle |
| 3 | [685. Redundant Connection II](https://leetcode.com/problems/redundant-connection-ii/) | 🔴 Hard | Directed cycle — harder variant with in-degree analysis |
| 4 | [802. Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | 🟡 Medium | Directed — find all nodes NOT part of a cycle (reverse the cycle logic) |
| 5 | [261. Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | 🟡 Medium | Undirected — valid tree = connected + no cycle (⚠️ Premium) |

> 💡 **684 is the must-do.** It elegantly combines cycle detection with Union-Find. 802 is the twist — instead of detecting cycles, you're finding nodes that *escape* them — a senior-level reframing of the same concept.

### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🎯 Comprehensive | [Graph Cycle Detection: DFS, Union Find & Topo Sort](https://www.youtube.com/watch?v=lvMseLfP0Jw) | Covers all 3 methods in one video — great for comparison |
| 🎯 Striver (TakeUForward) | [Detect Cycle in Directed Graph using BFS — Kahn's](https://www.youtube.com/watch?v=V6GxfKDyLBM) | Step-by-step directed graph cycle via in-degree |
| 🔵 William Fiset | [WilliamFiset Graph Theory Playlist](https://www.youtube.com/channel/UCD8yeTczadqdARzQUp29PJw) | Full graph theory course — reference for deep dives |

---

## 7. Union-Find (Disjoint Set Union)

### Theory
Union-Find (DSU) is a data structure that maintains a collection of **disjoint (non-overlapping) sets**. It efficiently supports two operations:
- **Find(x)**: Which set does `x` belong to? (returns the root/representative)
- **Union(x, y)**: Merge the sets containing `x` and `y`

Two key optimizations make it nearly O(1) per operation:
1. **Path Compression**: When finding root, make every node point directly to root
2. **Union by Rank**: Always attach smaller tree under larger tree

### Algorithm

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))   # Each node is its own parent initially
        self.rank = [0] * n            # Tree height approximation
        self.components = n            # Number of connected components

    def find(self, x):
        # Path compression: make x point directly to root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Recursive compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same component (would create cycle)

        # Union by rank: attach smaller tree under larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.components -= 1
        return True  # Successfully merged

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

### Complexity
| Operation | Naive | With Path Compression + Union by Rank |
|-----------|-------|----------------------------------------|
| **Find** | O(n) | O(α(n)) ≈ **O(1)** amortized |
| **Union** | O(n) | O(α(n)) ≈ **O(1)** amortized |
| **Space** | O(n) | O(n) |

> α(n) is the **inverse Ackermann function** — grows incredibly slowly (≤ 4 for any practical n). Effectively constant.

### Step-by-Step Example

**Graph edges:** `(0,1), (1,2), (3,4), (2,3)`  
**n=5 nodes**

**Initial state:**
```
parent: [0, 1, 2, 3, 4]   (each node is its own root)
rank:   [0, 0, 0, 0, 0]
components: 5
```

**Union(0, 1):**
```
find(0)=0, find(1)=1 → different roots
rank[0]==rank[1] → attach 1 under 0, rank[0]++
parent: [0, 0, 2, 3, 4]
rank:   [1, 0, 0, 0, 0]
components: 4
```

**Union(1, 2):**
```
find(1) → parent[1]=0 → find(0)=0 (root)
find(2)=2
rank[0]=1 > rank[2]=0 → attach 2 under 0
parent: [0, 0, 0, 3, 4]
rank:   [1, 0, 0, 0, 0]
components: 3
```

**Union(3, 4):**
```
find(3)=3, find(4)=4 → different
rank equal → attach 4 under 3, rank[3]++
parent: [0, 0, 0, 3, 3]
rank:   [1, 0, 0, 1, 0]
components: 2
```

**Union(2, 3):**
```
find(2) → parent[2]=0 → root=0
find(3)=3
rank[0]=1 == rank[3]=1 → attach 3 under 0, rank[0]++
parent: [0, 0, 0, 0, 3]
rank:   [2, 0, 0, 1, 0]
components: 1
```

**Path compression in action — find(4):**
```
find(4) → parent[4]=3 → find(3) → parent[3]=0 → find(0)=0 (root)
After compression: parent[4] = 0  ← directly points to root now!
parent: [0, 0, 0, 0, 0]   ← fully compressed!
```

**Final: all 5 nodes in one component ✓**

### Key Interview Patterns
- **LeetCode 547 (Number of Provinces)**: Count `components` after all unions
- **LeetCode 684 (Redundant Connection)**: Union returns False → that edge creates cycle
- **Kruskal's MST**: Sort edges by weight, union greedily, skip if already connected
- **LeetCode 721 (Accounts Merge)**: Union emails belonging to same account

### Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | 🟡 Medium | Classic Union-Find — count remaining components |
| 2 | [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | 🟡 Medium | Detect the edge that creates a cycle using Union-Find |
| 3 | [721. Accounts Merge](https://leetcode.com/problems/accounts-merge/) | 🟡 Medium | Union-Find on string keys — group accounts by shared emails |
| 4 | [1319. Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | 🟡 Medium | Count extra edges and components — elegant Union-Find application |
| 5 | [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | 🟡 Medium | Kruskal's MST using Union-Find — build graph implicitly |
| 6 | [990. Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) | 🟡 Medium | Union-Find on equations — process `==` first, then validate `!=` |


### Video References

| Channel | Video | Focus |
|---------|-------|-------|
| 🎯 Striver (TakeUForward) | [Disjoint Set \| Union Find \| Union by Rank \| Path Compression](https://www.youtube.com/watch?v=0JE7hxr8c5c) | Best structured explanation of both optimizations |
| 📊 Visual Explanation | [Union Find Visually Explained](https://www.youtube.com/watch?v=92UpvDXc8fs) | Animation-first, ideal if you're a visual learner |
| 🎯 Striver | [Disjoint Set — Detect Cycle in Undirected Graph](https://www.youtube.com/watch?v=CbPY2MOBbSk) | Combines Union-Find with cycle detection — two topics at once |

---

## Quick Reference — Complexity Summary

| Algorithm | Time | Space | Key Data Structure |
|-----------|------|-------|--------------------|
| BFS | O(V+E) | O(V) | Queue |
| DFS | O(V+E) | O(V) | Stack / Recursion |
| Dijkstra | O((V+E) log V) | O(V) | Min-Heap |
| A* | O(E log V) | O(V) | Min-Heap + Heuristic |
| Topo Sort (Kahn) | O(V+E) | O(V) | Queue + In-degree |
| Topo Sort (DFS) | O(V+E) | O(V) | DFS Stack |
| Cycle Detection | O(V+E) | O(V) | DFS Colors |
| Union-Find | O(α(n)) per op | O(n) | Array |

---

## Decision Guide — Which Algorithm to Use?

```
Is the graph weighted?
├── NO → Use BFS (shortest path by edges)
└── YES
    ├── All weights non-negative?
    │   ├── Single target on grid/map? → Use A*
    │   └── General graph? → Use Dijkstra
    └── Negative weights? → Use Bellman-Ford

Need ordering/scheduling?
└── Use Topological Sort (check for cycle with Kahn's)

Need connected components / cycle in undirected?
└── Use Union-Find (or DFS)

Need cycle in directed graph?
└── Use DFS with 3-color marking

Need to explore all paths / detect reachability?
└── Use DFS

Need level-by-level / shortest unweighted path?
└── Use BFS
```

---

## 8. Grid Problems — End-to-End Walkthroughs

> These three problems cover the four core grid patterns. Each walkthrough uses the universal template — notice how the skeleton barely changes between problems.

---

### Problem 1 — LeetCode 200: Number of Islands
🔗 [https://leetcode.com/problems/number-of-islands/](https://leetcode.com/problems/number-of-islands/)
**Difficulty:** 🟡 Medium | **Pattern:** DFS Flood Fill | **Direction:** 4-dir

#### Problem Statement
Given a 2D grid of `'1'` (land) and `'0'` (water), return the number of islands. An island is surrounded by water and formed by connecting adjacent land cells horizontally or vertically.

#### Checklist Applied
```
1. Each cell = a node. Value '1' = land, '0' = water.
2. Valid to visit: in bounds + is '1' + not yet visited
3. 4-dir (no diagonals — "horizontally or vertically")
4. DFS — we need to explore/count regions, not find shortest path
5. Single source per island (outer loop triggers one DFS per island)
6. Need a count, not a distance
```

#### Grid Used
```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

#### Solution
```python
from typing import List

def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]   # 4-dir only

    def dfs(r, c):
        # Three guards — always in this order
        if not (0 <= r < rows and 0 <= c < cols):  # out of bounds
            return
        if (r, c) in visited:                       # already seen
            return
        if grid[r][c] == '0':                       # water cell
            return

        visited.add((r, c))                         # mark visited

        for dr, dc in dirs:
            dfs(r + dr, c + dc)                     # flood fill all 4 neighbours

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)   # sinks the entire island
                count += 1  # only increments once per island

    return count
```

#### Step-by-Step Execution
```
Grid:
(0,0)(0,1)  .    .    .
(1,0)(1,1)  .    .    .
  .    .  (2,2)  .    .
  .    .    .  (3,3)(3,4)

Outer loop hits (0,0): grid='1', not visited → DFS(0,0)
  DFS(0,0): mark visited, recurse on neighbours
    DFS(-1,0): OUT OF BOUNDS → return
    DFS(1,0):  '1', not visited → mark, recurse
      DFS(2,0): '0' → return
      DFS(0,0): visited → return
      DFS(1,-1): OUT OF BOUNDS → return
      DFS(1,1): '1', not visited → mark, recurse
        DFS(0,1): '1', not visited → mark, recurse
          ... all neighbours are visited or '0'
        DFS(2,1): '0' → return
        DFS(1,0): visited → return
        DFS(1,2): '0' → return
    DFS(-1,0): already covered
    DFS(0,1): already visited
    DFS(0,-1): OUT OF BOUNDS → return
  count++ → count = 1  ✓  (Island 1: cells (0,0)(0,1)(1,0)(1,1))

Outer loop hits (0,1): already visited → skip
...
Outer loop hits (2,2): '1', not visited → DFS(2,2)
  DFS(2,2): mark, all neighbours are '0' or OOB → returns immediately
  count++ → count = 2  ✓  (Island 2: just cell (2,2))

Outer loop hits (3,3): '1', not visited → DFS(3,3)
  DFS(3,3): mark, recurse on (3,4)
    DFS(3,4): mark, all neighbours visited or '0'
  count++ → count = 3  ✓  (Island 3: cells (3,3)(3,4))

Final answer: 3
```

#### Complexity
| | Value |
|---|---|
| **Time** | O(rows × cols) — every cell visited at most once |
| **Space** | O(rows × cols) — visited set + recursion stack depth |

#### Key Insight
The outer `for` loop is what makes this work. It ensures you don't miss any island. The DFS just "floods" everything connected — by the time DFS returns, the entire island is in `visited`. The next unvisited `'1'` the outer loop finds **must** be a new, separate island.

---

### Problem 2 — LeetCode 994: Rotting Oranges
🔗 [https://leetcode.com/problems/rotting-oranges/](https://leetcode.com/problems/rotting-oranges/)
**Difficulty:** 🟡 Medium | **Pattern:** Multi-Source BFS | **Direction:** 4-dir

#### Problem Statement
A grid contains: `0` = empty, `1` = fresh orange, `2` = rotten orange. Every minute, a rotten orange rots all adjacent fresh oranges. Return the minimum minutes until no fresh orange remains. Return `-1` if impossible.

#### Checklist Applied
```
1. Each cell = a node. 0=empty, 1=fresh, 2=rotten.
2. Valid to visit: in bounds + is fresh (==1) + not visited
3. 4-dir (adjacent = horizontal/vertical only)
4. BFS — "minimum minutes" = shortest time = BFS levels
5. MULTI-SOURCE — all rotten oranges rot simultaneously → push ALL of them at step 0
6. Need the level count (minutes), and check if any fresh remain
```

#### Grid Used
```
2 1 1
1 1 0
0 1 1
```

#### Solution
```python
from collections import deque
from typing import List

def orangesRotting(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    queue = deque()
    fresh_count = 0

    # Seed the queue with ALL rotten oranges at time=0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))   # (row, col, time)
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0   # No fresh oranges — already done

    max_time = 0

    while queue:
        r, c, time = queue.popleft()

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue              # out of bounds
            if grid[nr][nc] != 1:
                continue              # not a fresh orange (empty or already rotten)

            grid[nr][nc] = 2          # rot it (mutate grid = visited marker)
            fresh_count -= 1
            max_time = max(max_time, time + 1)
            queue.append((nr, nc, time + 1))

    return max_time if fresh_count == 0 else -1
```

#### Step-by-Step Execution
```
Grid:
2 1 1
1 1 0
0 1 1

Initial scan:
  Rotten at (0,0) → queue = [(0,0,t=0)]
  Fresh count = 6

Minute 0 — Process (0,0):
  Neighbours: (1,0)=fresh✓  (0,1)=fresh✓
  → Rot (1,0): fresh=5, queue: [(1,0,t=1)]
  → Rot (0,1): fresh=4, queue: [(1,0,t=1),(0,1,t=1)]

Grid after minute 0:
2 2 1
2 1 0
0 1 1

Minute 1 — Process (1,0,t=1) and (0,1,t=1):
  From (1,0): (0,0)=rotten, (2,0)=empty, (1,1)=fresh✓
    → Rot (1,1): fresh=3, enqueue (1,1,t=2)
  From (0,1): (0,0)=rotten, (0,2)=fresh✓, (1,1)=just rotted
    → Rot (0,2): fresh=2, enqueue (0,2,t=2)

Grid after minute 1:
2 2 2
2 2 0
0 1 1

Minute 2 — Process (1,1,t=2) and (0,2,t=2):
  From (1,1): (2,1)=fresh✓
    → Rot (2,1): fresh=1, enqueue (2,1,t=3)
  From (0,2): all neighbours rotten/empty/OOB

Grid after minute 2:
2 2 2
2 2 0
0 2 1

Minute 3 — Process (2,1,t=3):
  From (2,1): (2,2)=fresh✓
    → Rot (2,2): fresh=0, enqueue (2,2,t=4)

Minute 4 — Process (2,2,t=4):
  No fresh neighbours

Queue empty. fresh_count = 0. max_time = 4.
Return 4 ✓
```

#### Why Multi-Source?
If you started BFS from just one rotten orange, you'd get the wrong answer — the rot spreads **from all rotten cells simultaneously**, not one at a time. Seeding the queue with all sources at `t=0` models this perfectly. This is the defining trick of multi-source BFS.

#### Complexity
| | Value |
|---|---|
| **Time** | O(rows × cols) — every cell processed at most once |
| **Space** | O(rows × cols) — queue size at worst holds all cells |

---

### Problem 3 — LeetCode 417: Pacific Atlantic Water Flow
🔗 [https://leetcode.com/problems/pacific-atlantic-water-flow/](https://leetcode.com/problems/pacific-atlantic-water-flow/)
**Difficulty:** 🟡 Medium | **Pattern:** Reverse Multi-Source DFS from Two Borders | **Direction:** 4-dir

#### Problem Statement
Rain water flows from a cell to adjacent cells with **equal or lower height**. The Pacific Ocean touches the top and left borders. The Atlantic touches the bottom and right borders. Return all cells from which water can flow to **both** oceans.

#### The Key Insight — Think Backwards
The naive approach (DFS from every cell, check if it can reach both oceans) is O((m×n)²) — too slow.

**Reverse the problem:** Instead of asking "can water flow FROM this cell TO the ocean?", ask "can water flow FROM the ocean TO this cell?" — but uphill (reverse direction). Water flows downhill normally, so reversed = water flows uphill, meaning we only step to cells with **equal or greater** height.

```
Normal:    cell → neighbour if neighbour height <= cell height
Reversed:  ocean → cell if cell height >= ocean height
```

Run this reversed DFS from **both** ocean borders. Any cell reachable from both sets = answer.

#### Checklist Applied
```
1. Each cell = a node. Value = height.
2. Valid to visit: in bounds + not visited + height >= current cell (reversed flow)
3. 4-dir
4. DFS — we're exploring reachability, not shortest path
5. TWO separate multi-source DFS runs: one from Pacific border, one from Atlantic border
6. Answer = intersection of both reachable sets
```

#### Grid Used
```
Heights:
1 2 2 3 5
3 2 3 4 4
2 4 5 3 1
6 7 1 4 5
5 1 1 2 4
```

#### Solution
```python
from typing import List

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    rows, cols = len(heights), len(heights[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    def dfs(r, c, visited):
        visited.add((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue                             # out of bounds
            if (nr, nc) in visited:
                continue                             # already reached
            if heights[nr][nc] < heights[r][c]:     # can't flow uphill (reversed logic)
                continue
            dfs(nr, nc, visited)

    pacific  = set()   # cells reachable from Pacific border
    atlantic = set()   # cells reachable from Atlantic border

    # Seed Pacific: top row + left column
    for c in range(cols):
        dfs(0, c, pacific)          # top row
    for r in range(rows):
        dfs(r, 0, pacific)          # left column

    # Seed Atlantic: bottom row + right column
    for c in range(cols):
        dfs(rows - 1, c, atlantic)  # bottom row
    for r in range(rows):
        dfs(r, cols - 1, atlantic)  # right column

    # Intersection = can reach both
    return [[r, c] for r in range(rows)
                   for c in range(cols)
                   if (r, c) in pacific and (r, c) in atlantic]
```

#### Step-by-Step Execution (abbreviated)

```
Grid (heights):
1 2 2 3 5
3 2 3 4 4
2 4 5 3 1
6 7 1 4 5
5 1 1 2 4

Pacific seeds (top row + left col):
  Top row:    (0,0)(0,1)(0,2)(0,3)(0,4)
  Left col:   (1,0)(2,0)(3,0)(4,0)

DFS from Pacific border — can only move to cells with height ≥ current:
  From (0,0)[h=1]: can go to (1,0)[h=3]✓ → from (1,0): (2,0)[h=2]✗, (3,0)[h=6]✓ → ...
  From (0,4)[h=5]: can go to (1,4)[h=4]✗ (4 < 5)
  From (3,0)[h=6]: can go to (4,0)[h=5]✗, (3,1)[h=7]✓ → from (3,1): (2,1)[h=4]✗, (4,1)[h=1]✗
  ...
Pacific reachable = {(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0),(1,1),(3,1),...}

Atlantic seeds (bottom row + right col):
  Bottom row: (4,0)(4,1)(4,2)(4,3)(4,4)
  Right col:  (0,4)(1,4)(2,4)(3,4)

DFS from Atlantic border — same uphill logic:
  From (4,4)[h=4]: (3,4)[h=5]✓ → (2,4)[h=1]✗, (3,3)[h=4]✓ → ...
  From (0,4)[h=5]: already seeded ...
Atlantic reachable = {(4,0),(4,1),...,(3,4),(2,3),(1,3),(1,4),(0,4),(3,3),(2,2),...}

Intersection (both sets) → answer cells:
  (0,4) (1,3) (1,4) (2,2) (3,0) (3,1) (3,4) (4,4) → [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[3,4],[4,4]]
```

#### Why This Works
By running DFS backwards from ocean borders, every cell in `pacific` is guaranteed to be able to drain to Pacific (by reversing your steps downhill). The intersection gives exactly the cells that can drain both ways.

#### Complexity
| | Value |
|---|---|
| **Time** | O(rows × cols) — each cell visited at most twice (once per ocean) |
| **Space** | O(rows × cols) — two visited sets |

---

### Grid Patterns — Final Summary

| Problem | Pattern | Direction | Algorithm | Key Trick |
|---------|---------|-----------|-----------|-----------|
| 200. Number of Islands | Flood fill / count components | 4-dir | DFS | Outer loop triggers one DFS per island |
| 994. Rotting Oranges | Multi-source shortest time | 4-dir | BFS | Seed ALL sources at t=0 |
| 417. Pacific Atlantic | Two-border reachability | 4-dir | DFS | Reverse the flow direction; find intersection |
| 1091. Shortest Path in Binary Matrix | Single-source shortest path | **8-dir** | BFS | 8-directional dirs, return step count |
| 542. 01 Matrix | Distance to nearest target | 4-dir | Multi-source BFS | Seed all `0`s, spread outward |
| 130. Surrounded Regions | Boundary-safe flood fill | 4-dir | DFS | DFS from borders first, then flip interior |

---
