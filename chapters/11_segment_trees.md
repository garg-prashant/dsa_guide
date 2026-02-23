# Chapter 11: Segment Trees

> *"When you need range queries and point updates (or range updates) in O(log n), a segment tree is the tool."*

---

## 11.1 Why Segment Trees Matter

A **segment tree** is a binary tree where each node represents an **interval** of the array. It supports **range queries** (e.g., sum, min, max over [L, R]) and **point updates** (change one element) in **O(log n)**. With **lazy propagation**, **range updates** (add x to all elements in [L, R]) also become O(log n). Used in competitive programming and some interview problems (range sum queries, mutable array). Simpler alternative for prefix/sum updates: **Fenwick tree** (Chapter 12). Use a segment tree when you need arbitrary range queries (sum/min/max) and updates.

---

## 11.2 Structure

- **Leaf nodes** = single elements (range of length 1).
- **Internal node** = merge of its two children (e.g., left sum + right sum).
- **Root** = full range [0, n-1].
- Stored in an array: for node at index `i`, left child at `2*i`, right at `2*i+1` (1-indexed) or `2*i+1` and `2*i+2` (0-indexed).

```
Array: [1, 3, 2, 5, 4]
Range sum tree (conceptually):
        [0:4]=15
       /        \
   [0:2]=6      [3:4]=9
   /    \         /   \
[0:1]=4 [2]=2  [3]=5 [4]=4
 /  \
[0]=1 [1]=3
```

---

## 11.3 Build, Point Update, Range Query (Sum)

```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i + 1]

    def update(self, index, value):
        i = self.size + index
        self.tree[i] = value
        i //= 2
        while i:
            self.tree[i] = self.tree[2*i] + self.tree[2*i + 1]
            i //= 2

    def query(self, left, right):
        # [left, right] inclusive
        left += self.size
        right += self.size
        s = 0
        while left <= right:
            if left % 2 == 1:
                s += self.tree[left]
                left += 1
            if right % 2 == 0:
                s += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        return s
```

**Build:** O(n). **Update:** O(log n). **Query:** O(log n). **Space:** O(n).

---

## 11.4 Range Min/Max

Same structure; use `min` or `max` instead of `+`. Initialize unused leaves to `float('inf')` for min or `float('-inf')` for max so they don't affect the result.

---

## 11.5 Lazy Propagation (Range Update)

To add a value to every element in [L, R], we **lazy propagate**: store a "pending" value at a node and only push it down when we traverse through that node. This keeps range add (and range query) at O(log n).

Concept: each node has `value` and `lazy`. When updating range [l, r] with +d: if current node's segment is entirely inside [l, r], add d to lazy and update value by d * (segment length); else push lazy to children, then recurse and merge. Query: when traversing, push lazy down before going to children.

Implementation is longer; pattern: **push(node)** applies lazy to children and clears lazy; call push before recursing.

---

## 11.6 When to Use Segment Tree vs Fenwick Tree

| Need | Prefer |
|------|--------|
| Range sum + point/range update | Both; Fenwick simpler for sum |
| Range min/max query | Segment tree (Fenwick doesn't do general range min/max) |
| Lazy range update | Segment tree with lazy propagation |

---

## 11.7 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(n) |
| Point update | O(log n) | O(1) |
| Range query | O(log n) | O(1) |
| Range update (lazy) | O(log n) | O(1) |

---

## Practice Exercises

**E1.** Range Sum Query - Mutable — point update, range sum. Segment tree or Fenwick.

**E2.** Maximum subarray sum with point updates — segment tree storing per-segment: sum, max prefix, max suffix, max subarray; merge in O(1).

**E3.** Count of Smaller Numbers After Self (alternative) — coordinate compress, then for each element from right, query segment tree for count in [0, value-1], then update tree at value. Or use merge sort / Fenwick.

---

## Chapter Summary

| Use Case | Operation |
|----------|-----------|
| Range sum/min/max | Query [L,R] in O(log n) |
| Point update | Update index, propagate up |
| Range update | Lazy propagation |

**Previous:** [Chapter 10 → Union-Find](10_union_find.md) | **Next:** [Chapter 12 → Fenwick Trees](12_fenwick_trees.md)
