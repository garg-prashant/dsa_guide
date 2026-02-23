# Chapter 7: Heaps & Priority Queues

> *"A heap gives you the best of the current set in O(log n). That's why it powers 'top K' and shortest path."*

---

## 7.1 Why Heaps Matter

A **heap** is a complete binary tree that satisfies the **heap property**: in a **min-heap**, every parent is ≤ its children (smallest at root); in a **max-heap**, every parent ≥ its children (largest at root). It's the backing structure for a **priority queue** — insert in O(log n), get/remove the min (or max) in O(log n). Interviews love "K largest/smallest", "merge K sorted lists", "median of stream", and "Dijkstra" (see **Chapter 21**). You rarely implement a heap from scratch; Python's `heapq` is a min-heap. Knowing the operations and when to use a heap is what matters.

---

## 7.2 Heap Property and Shape

**Shape:** Complete binary tree — all levels full except possibly the last, which is filled left to right. So we can store the tree in an **array**: for index `i`, left child at `2*i+1`, right at `2*i+2`, parent at `(i-1)//2`.

**Min-heap:** `A[parent] ≤ A[child]` → minimum at index 0.

**Max-heap:** `A[parent] ≥ A[child]` → maximum at index 0.

```
Min-heap (array): [1, 3, 2, 6, 4, 5]
        1
       / \
      3   2
     / \ /
    6  4 5
```

---

## 7.3 Core Operations: Heapify Up and Down

- **Heapify up (sift up):** After inserting at the end, swap with parent until heap property holds. O(log n).
- **Heapify down (sift down):** After replacing root (e.g., for extract-min), swap with the **smaller** child until heap property holds. O(log n).

**Extract-min:** Swap root with last element, pop last, then heapify down from root.

**Insert:** Append at end, then heapify up.

### Worked Example: Insert 0 into a Min-Heap

Heap (array): `[1, 3, 2, 6, 4, 5]`. Tree view:
```
        1
       / \
      3   2
     / \ /
    6  4 5
```
Insert 0 at end → `[1, 3, 2, 6, 4, 5, 0]`. Sift up: 0 < 2, swap with 2; 0 < 1, swap with 1.
```
  After insert at end:     After sift up (0 bubbles up):
        1                       0
       / \                     / \
      3   2                   1   2
     / \ / \                 / \ / \
    6  4 5  0               6  4 5  3
```
Array becomes `[0, 1, 2, 6, 4, 5, 3]`.

### Worked Example: Extract-Min

Start with `[0, 1, 2, 6, 4, 5, 3]`. Swap root (0) with last (3); pop last → min=0, array `[3, 1, 2, 6, 4, 5]`. Sift down 3: swap with smaller child (1) → `[1, 3, 2, 6, 4, 5]`; 3 has children 6, 4; 3 < 4 and 3 < 6, so stop. New min-heap: `[1, 3, 2, 6, 4, 5]`.

---

## 7.4 Python's heapq Module

`heapq` keeps a **min-heap** only. It does **not** provide a max-heap directly; use the "negate" trick: push `-x`, pop `-heapq.heappop(heap)`.

```python
import heapq

# Min-heap (default)
h = []
heapq.heappush(h, 5)
heapq.heappush(h, 2)
heapq.heappush(h, 8)
heapq.heappop(h)   # 2
heapq.heappop(h)   # 5

# Max-heap trick: store (-priority, item)
h = []
heapq.heappush(h, (-5, "task5"))
heapq.heappush(h, (-2, "task2"))
heapq.heappush(h, (-8, "task8"))
_, item = heapq.heappop(h)   # "task8"

# Heapify existing list in-place: O(n)
arr = [3, 1, 4, 1, 5]
heapq.heapify(arr)   # arr is now a min-heap

# nlargest / nsmallest (uses heap internally)
heapq.nlargest(2, [3, 1, 4, 1, 5])   # [5, 4]
heapq.nsmallest(2, [3, 1, 4, 1, 5])   # [1, 1]
```

**Important:** `heapq` compares by value. For objects, use `(priority, counter, obj)` or implement `__lt__` so that ties don't cause comparison of non-comparable objects.

```python
# Push (priority, count, task) to avoid comparing tasks when priorities tie
import itertools
counter = itertools.count()
heapq.heappush(h, (priority, next(counter), task))
```

---

## 7.5 Implementation: Min-Heap from Scratch

Useful to know for interviews that ask "implement a heap".

```python
class MinHeap:
    def __init__(self):
        self.data = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def push(self, x):
        self.data.append(x)
        self._sift_up(len(self.data) - 1)

    def _sift_up(self, i):
        while i > 0 and self.data[i] < self.data[self._parent(i)]:
            p = self._parent(i)
            self._swap(i, p)
            i = p

    def pop(self):
        if not self.data:
            raise IndexError("heap is empty")
        self._swap(0, len(self.data) - 1)
        val = self.data.pop()
        if self.data:
            self._sift_down(0)
        return val

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left = self._left(i)
            right = self._right(i)
            smallest = i
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def peek(self):
        return self.data[0] if self.data else None
```

---

## 7.6 Heap Sort

1. Heapify the array into a max-heap (or use min-heap and collect in reverse).
2. Repeatedly extract the max: swap with last, decrease "size", sift down. Put extracted max at the end.

Result: sorted array in place. Time O(n log n), space O(1) if we do in-place.

```python
def heap_sort(arr):
    n = len(arr)
    heapq.heapify(arr)   # min-heap
    return [heapq.heappop(arr) for _ in range(n)]
# Or build max-heap and extract to end; above uses extra space for result.
```

For in-place max-heap sort: build max-heap (sift down from last non-leaf to 0), then for i from n-1 down to 1: swap arr[0] with arr[i], sift_down(0, i).

---

## 7.7 Applications

### K largest (or K smallest) elements

**K largest:** Keep a **min-heap of size K**. For each element: if heap size < K, push; else if element > heap min, pop min and push element. At the end, the heap contains the K largest. O(n log K).

```python
def top_k_largest(nums, k):
    if k >= len(nums):
        return nums
    heap = nums[:k]
    heapq.heapify(heap)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)   # pop min, push x
    return heap
```

**K smallest:** Use a **max-heap of size K** (store negatives with heapq) and keep the K smallest.

### Merge K sorted lists

Push the first element of each list (with list index and position) into a min-heap. Pop the smallest, push the next from that list. Repeat. O(N log K) where N = total elements, K = number of lists.

```python
def merge_k_sorted(lists):
    import heapq
    heap = []
    for i, L in enumerate(lists):
        if L:
            heapq.heappush(heap, (L[0], i, 0))
    out = []
    while heap:
        val, list_i, idx = heapq.heappop(heap)
        out.append(val)
        if idx + 1 < len(lists[list_i]):
            nxt = lists[list_i][idx + 1]
            heapq.heappush(heap, (nxt, list_i, idx + 1))
    return out
```

### Find median from data stream

Maintain **lower half** in a **max-heap** and **upper half** in a **min-heap**. Keep sizes equal (or lower has one more). Median = max of lower (or average of both tops if equal size). See **Chapter 4** for a hint; full design is a classic problem.

---

## 7.8 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| push | O(log n) | O(1) |
| pop (extract min/max) | O(log n) | O(1) |
| peek | O(1) | O(1) |
| heapify (build from list) | O(n) | O(1) |
| heap sort | O(n log n) | O(1) in-place |
| K largest with size-K heap | O(n log K) | O(K) |

---

## 7.9 When to Use a Heap

- **Kth largest / smallest** → min-heap of size K (for largest) or max-heap of size K (for smallest).
- **Merge K sorted** → min-heap over heads of each list.
- **Median / percentiles** → two heaps (lower half max-heap, upper half min-heap).
- **Dijkstra / BFS with weights** → priority queue by distance (see **Chapter 21**).
- **Scheduling / "earliest deadline"** → priority queue by time or priority.

---

## 7.10 Gotchas

- **heapq is min-heap only.** For max-heap, negate keys or use `(priority, item)` and negate priority.
- **Stability:** heapq doesn't guarantee stable sort; equal priorities can be popped in any order.
- **Mutable objects:** If you push objects that change, the heap can become invalid. Prefer (priority, id or counter, object).

---

## Practice Exercises

### Easy

**E1.** Kth Largest Element in an Array — use a min-heap of size K.

**E2.** Last Stone Weight — repeatedly take two largest, smash them; return the last remaining weight. Max-heap (negate values).

**E3.** Min Cost to Connect Sticks (or similar): combine two smallest repeatedly. Min-heap, pop two, push sum, repeat.

### Medium

**E4.** Merge K Sorted Lists — min-heap over first node of each list.

**E5.** Top K Frequent Elements — count frequencies, then keep min-heap of size K by frequency (push (freq, num), pop when size > K).

**E6.** Find Median from Data Stream — two heaps: max-heap for lower half, min-heap for upper half; balance after each addNum.

**E7.** K Closest Points to Origin — min-heap by distance (or quick select). Heap: push all (dist², point), pop K times.

### Hard

**E8.** Merge K Sorted Lists (if not done) or Trapping Rain Water II (3D: elevation map; boundary in min-heap, expand inward).

**E9.** Minimum Cost to Hire K Workers — ratio of wage/quality; sort by ratio, for each worker as "captain" take K-1 workers with smallest quality to the left (heap).

---

## Chapter Summary

| Pattern | Use Case |
|---------|----------|
| Min-heap size K | K largest elements |
| Max-heap size K (negate) | K smallest elements |
| Two heaps | Median of stream |
| Heap over list heads | Merge K sorted lists |
| Priority queue | Dijkstra, scheduling |

**Previous:** [Chapter 6 → Trees](06_trees.md) | **Next:** [Chapter 8 → Graphs](08_graphs.md)
