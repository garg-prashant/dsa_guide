# Chapter 10: Union-Find (Disjoint Set Union)

> *"Union-Find answers one question fast: 'Are these two in the same group?' And it merges groups in nearly O(1)."*

---

## 10.1 Why Union-Find Matters

**Union-Find** (Disjoint Set Union, DSU) keeps a partition of elements into **disjoint sets**. It supports: **find(u)** — which set does u belong to? **union(u, v)** — merge the sets containing u and v. With **path compression** and **union by rank** (or size), both operations are **nearly O(1)** amortized. It's the go-to for "connect components over time", "is there a path between u and v?" (when you only add edges), number of connected components, and **Kruskal's MST** (see **Chapter 21**). Classic problems: Number of Islands (with union), redundant connection, accounts merge.

---

## 10.2 Interface

- **parent[i]** = representative (root) of the set containing i, or parent of i on the path to the root.
- **find(x):** Return the root of x's set; use path compression so future finds are fast.
- **union(x, y):** Merge the sets containing x and y; use union by rank (or size) so the tree stays shallow.

Initially: each element is its own set, so **parent[i] = i** (and optionally **rank[i] = 0**).

---

## 10.3 Naive Implementation (No Optimizations)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry
```

Without path compression, find can be O(n). With path compression only, amortized is O(α(n)) ≈ O(1). Adding union by rank keeps the tree depth small and makes the analysis clean.

---

## 10.4 Full Implementation: Path Compression + Union by Rank

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n   # number of disjoint sets

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Union by rank:** Attach the smaller (by rank) tree under the larger. Rank = upper bound on depth. **Path compression:** During find, make every node on the path point directly to the root. Together: amortized O(α(n)) per operation, where α is inverse Ackermann (effectively constant).

**Union by size:** Same idea; keep **size[i]** for the root of each set; attach smaller set under larger. Also gives O(α(n)).

---

## 10.5 Typical Usage

**Number of connected components after adding edges:** Start with n sets. For each edge (u, v), union(u, v). Answer = uf.count (or count roots where parent[i] == i).

**Is graph connected?** After processing all edges, check uf.count == 1.

**Kruskal's MST:** Sort edges by weight; add edge (u, v) if find(u) != find(v), then union(u, v). See **Chapter 21**.

**Redundant connection:** Add edges one by one; when an edge (u, v) has find(u) == find(v) before adding, that edge forms a cycle (redundant).

---

## 10.6 Complexity Summary

| Operation | Time (amortized) | Space |
|-----------|------------------|-------|
| find | O(α(n)) ≈ O(1) | O(1) |
| union | O(α(n)) ≈ O(1) | O(1) |
| Construction | O(n) | O(n) |

---

## 10.7 When to Use Union-Find

- **Incremental connectivity:** Edges (or connections) added over time; answer "same component?" or "how many components?"
- **Undirected cycle detection:** If find(u) == find(v) before adding (u,v), adding would create a cycle.
- **Kruskal's MST:** Need to check "already connected?" and merge sets.
- **Grouping / equivalence:** "Merge these accounts", "same group as" — model as union and find.

---

## 10.8 Gotchas

- **0-indexed vs 1-indexed:** If input uses 1..n, use parent of size n+1 and use indices 1..n (or subtract 1 when calling union/find).
- **Count of sets:** Maintain `count` in union (decrement when merging two different sets). Or count roots at the end: `sum(1 for i in range(n) if uf.parent[i] == i)`.
- **Directed:** Union-Find is for **undirected** equivalence. For directed graphs use DFS/BFS or SCC.

---

## Practice Exercises

### Easy

**E1.** Number of Islands (alternative) — treat each '1' as a node; union with neighbors; count = number of sets. (Or use DFS as in **Chapter 8**.)

**E2.** Find if path exists — union all edges; check find(start) == find(end).

### Medium

**E3.** Redundant Connection — add edges; first edge that connects two already-connected nodes is the answer.

**E4.** Number of Connected Components in Undirected Graph — union all edges; return count.

**E5.** Accounts Merge — map email → component; union emails that appear in same list; then group by find(email).

### Hard

**E6.** Longest Consecutive Sequence (alternative: union adjacent numbers in a set) — put values in set; for each v, if v-1 not in set, union v with v+1, v+2, ... and track size. Or use hash map + expand (no DSU). DSU: for each v, if v+1 in set then union(v, v+1); return max size of a set.

**E7.** Kruskal's MST — sort edges, add if not connected, union. See **Chapter 21**.

---

## Chapter Summary

| Pattern | Use Case |
|---------|----------|
| find + union | Same set? Merge sets |
| Path compression + union by rank | Nearly O(1) amortized |
| Count sets | Maintain count or count roots |
| Add edges one by one | Connectivity, cycle detection, MST |

**Previous:** [Chapter 9 → Tries](09_tries.md) | **Next:** [Chapter 11 → Segment Trees](11_segment_trees.md)
