# Chapter 12: Fenwick Trees (Binary Indexed Trees)

> *"A Fenwick tree does one thing beautifully: prefix sums with point updates in O(log n)."*

---

## 12.1 Why Fenwick Trees Matter

A **Fenwick tree** (Binary Indexed Tree, BIT) supports **prefix sum** in O(log n) and **point update** (add a value to one index) in O(log n). It uses less code and cache-friendly indexing compared to a segment tree for this use case. Classic uses: range sum query mutable, count inversions, count smaller after self (with coordinate compression). Interviewers sometimes ask "range sum with updates" — Fenwick is the compact answer.

---

## 12.2 Idea

- **Prefix sum** without updates: precompute prefix array; query [0, i] in O(1); but point update would require O(n) to fix prefixes.
- **Fenwick:** Store a tree that aggregates ranges in a clever way so each index "covers" a range determined by the **lowbit** of its index.

**Lowbit:** `i & (-i)` — the lowest set bit of i. Example: 6 = 110 → lowbit = 2; 8 = 1000 → lowbit = 8.

- **tree[i]** stores the sum of a **segment** ending at index i: from (i - lowbit(i) + 1) to i, inclusive.
- **Query prefix [0, i]:** Add tree[i], then subtract lowbit repeatedly: i -= i & (-i), add tree[i], until i == 0. O(log n).
- **Point update at i (add delta):** Add delta to tree[i], then i += i & (-i), repeat until i > n. O(log n).

---

## 12.3 Implementation (1-indexed)

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def _lowbit(self, i):
        return i & (-i)

    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += self._lowbit(i)

    def query_prefix(self, i):
        """Sum of [1..i] inclusive (1-indexed)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= self._lowbit(i)
        return s

    def query_range(self, left, right):
        """Sum of [left, right] inclusive (1-indexed)."""
        return self.query_prefix(right) - self.query_prefix(left - 1)
```

**Range update (add d to [L, R]):** Use a **difference array** idea: maintain a BIT that stores differences. Add d at L, subtract d at R+1. Then prefix_sum(i) = value at i. So: update(L, d), update(R+1, -d). Range query becomes two prefix queries. (Or use two BITs for range add + range sum — see "range update range query" variants.)

---

## 12.4 0-indexed to 1-indexed

If your array is 0-indexed, call `update(i+1, delta)` and `query_prefix(i+1)` for prefix [0..i]. Range [l, r] (0-indexed): `query_prefix(r+1) - query_prefix(l)`.

---

## 12.5 Build from Array

Either: initialize tree to zeros and call update(i, arr[i-1]) for each i → O(n log n). Or: compute prefix sums, then set tree[i] = prefix[i] - prefix[i - lowbit(i)] → O(n).

---

## 12.6 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) or O(n log n) | O(n) |
| Point update | O(log n) | O(1) |
| Prefix query | O(log n) | O(1) |
| Range query [L,R] | O(log n) | O(1) |

---

## 12.7 When to Use

- **Range sum + point update** → Fenwick.
- **Count inversions** — compress values, then for each element from right, query count of elements already seen that are greater (update at index = value).
- **Count smaller after self** — same idea: process from right, query prefix(value-1), update(value, 1).

---

## Practice Exercises

**E1.** Range Sum Query - Mutable — Fenwick (or segment tree).

**E2.** Count of Smaller Numbers After Self — coordinate compress; BIT; for each from right, res[i] = query(value-1), update(value, 1).

**E3.** Count Inversions — BIT or merge sort.

---

## Chapter Summary

| Operation | Use |
|-----------|-----|
| update(i, d) | Point update |
| query_prefix(i) | Prefix sum |
| query_range(L, R) | query_prefix(R) - query_prefix(L-1) |

**Previous:** [Chapter 11 → Segment Trees](11_segment_trees.md) | **Next:** [Chapter 13 → Sorting](13_sorting.md)
