# Chapter 4: Queues & Deques

> *"A queue is fair — the first to arrive is the first to be served."*

---

## 4.1 What Is a Queue?

A **queue** is a First-In, First-Out (FIFO) data structure. Like a line at a coffee shop — the first person in line is the first to be served.

```
Enqueue 1, 2, 3, 4:

FRONT                   BACK
 ↓                       ↓
[1] ← [2] ← [3] ← [4]

Dequeue → 1 (front leaves first)
```

**Core operations:**
| Operation | Description | Time |
|-----------|-------------|------|
| `enqueue(x)` / `put(x)` | Add to back | O(1) |
| `dequeue()` / `get()` | Remove from front | O(1) |
| `peek()` | View front without removing | O(1) |
| `is_empty()` | Check if queue is empty | O(1) |

---

## 4.2 Python Implementation

### Using `collections.deque` (Recommended)

`deque` (double-ended queue) is the right tool. Python's `list` is a bad queue because `list.pop(0)` is O(n) — it shifts every element.

```python
from collections import deque

q = deque()

q.append(1)        # enqueue to back
q.append(2)
q.append(3)

print(q[0])        # peek front → 1
q.popleft()        # dequeue from front → 1  ← O(1)!
print(q)           # deque([2, 3])
```

### Queue as a Class

```python
from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, val):
        self._data.append(val)       # add to back

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()  # remove from front

    def peek(self):
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
```

---

## 4.3 The Deque: Double-Ended Queue

A **deque** supports O(1) insertion and deletion from **both** ends. It's more flexible than both a stack and a queue.

```python
from collections import deque

d = deque([1, 2, 3])

d.appendleft(0)    # add to front  → deque([0, 1, 2, 3])
d.append(4)        # add to back   → deque([0, 1, 2, 3, 4])
d.popleft()        # remove front  → 0
d.pop()            # remove back   → 4
d.rotate(1)        # rotate right  → deque([3, 1, 2])
d.rotate(-1)       # rotate left   → deque([1, 2, 3])
```

---

## 4.4 Priority Queue (Heap Queue)

A **priority queue** serves elements in order of their **priority**, not arrival order. The element with the highest priority (or lowest value) is always at the front.

Python's `heapq` implements a **min-heap** (smallest element first):

```python
import heapq

pq = []
heapq.heappush(pq, 3)
heapq.heappush(pq, 1)
heapq.heappush(pq, 4)
heapq.heappush(pq, 1)
heapq.heappush(pq, 5)

print(heapq.heappop(pq))  # 1 (smallest)
print(heapq.heappop(pq))  # 1
print(heapq.heappop(pq))  # 3

# Max-heap: negate values
max_pq = []
heapq.heappush(max_pq, -3)
heapq.heappush(max_pq, -1)
print(-heapq.heappop(max_pq))  # 3 (original max)

# Priority queue with custom priority
# Push (priority, value) tuples
tasks = []
heapq.heappush(tasks, (3, "low priority"))
heapq.heappush(tasks, (1, "urgent"))
heapq.heappush(tasks, (2, "medium"))
print(heapq.heappop(tasks))  # (1, 'urgent')
```

---

## 4.5 The Monotonic Deque — Sliding Window Maximum

This is one of the most elegant algorithmic patterns. It combines the deque's double-ended nature with monotonicity.

**Problem (LeetCode 239):** Given an array and window size k, find the maximum in each sliding window.

**Naïve approach:** O(n·k) — check each window.
**Deque approach:** O(n) — each element is pushed and popped at most once.

**Key Idea:** Maintain a deque of **indices** such that the corresponding values are in **decreasing order**. The front of the deque is always the maximum of the current window.

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Window [1, 3, -1]:   max = 3
Window [3, -1, -3]:  max = 3
Window [-1, -3, 5]:  max = 5
Window [-3, 5, 3]:   max = 5
Window [5, 3, 6]:    max = 6
Window [3, 6, 7]:    max = 7
```

```python
from collections import deque

def sliding_window_max(nums, k):
    """O(n) time, O(k) space."""
    dq = deque()    # stores indices, values are decreasing
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is fully formed
        if i >= k - 1:
            result.append(nums[dq[0]])  # front is always max

    return result

print(sliding_window_max([1,3,-1,-3,5,3,6,7], 3))
# [3, 3, 5, 5, 6, 7]
```

**Trace through (first 4 steps):**
```
i=0, num=1: dq=[], push 0. dq=[0]. i<k-1, no result.
i=1, num=3: nums[0]=1 < 3, pop 0. dq=[]. Push 1. dq=[1]. i<k-1.
i=2, num=-1: nums[1]=3 > -1, push 2. dq=[1,2]. i=k-1, result=[nums[1]]=3.
i=3, num=-3: nums[2]=-1 > -3, push 3. dq=[1,2,3]. dq[0]=1 ≥ 3-3+1=1, in window.
             result=[3, nums[1]]=3. → [3, 3]
```

---

## 4.6 BFS — The Queue's Most Important Application

**Breadth-First Search** uses a queue to explore nodes layer by layer. It finds the **shortest path** in an unweighted graph.

```python
from collections import deque

def bfs(graph, start):
    """
    Explore all nodes reachable from start, level by level.
    graph: adjacency list {node: [neighbors]}
    """
    visited = {start}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node)  # process current node

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### BFS for Shortest Path

```python
def shortest_path(graph, start, end):
    """Return minimum steps from start to end."""
    if start == end:
        return 0
    visited = {start}
    queue = deque([(start, 0)])  # (node, steps)

    while queue:
        node, steps = queue.popleft()
        for neighbor in graph[node]:
            if neighbor == end:
                return steps + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, steps + 1))

    return -1  # no path exists
```

---

## 4.7 Classic Problems, Fully Solved

### Problem 1: Binary Tree Level Order Traversal

```python
from collections import deque

def level_order(root):
    """Return list of lists, each inner list is one level. O(n)."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)  # number of nodes at this level
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(level)

    return result
```

---

### Problem 2: Rotting Oranges (Multi-Source BFS)

*Given a grid where 0=empty, 1=fresh orange, 2=rotten orange. Rotten oranges rot adjacent fresh ones each minute. Return minutes until all fresh are rotten, or -1.*

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    # Find all initially rotten oranges and count fresh
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    max_time = 0

    while queue:
        r, c, time = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2  # mark rotten
                fresh -= 1
                max_time = max(max_time, time + 1)
                queue.append((nr, nc, time + 1))

    return max_time if fresh == 0 else -1
```

---

### Problem 3: Implement Queue Using Two Stacks

```python
class MyQueue:
    """
    Amortized O(1) per operation.
    Use two stacks: inbox (for push) and outbox (for pop).
    Transfer inbox → outbox only when outbox is empty.
    """
    def __init__(self):
        self.inbox = []   # new elements go here
        self.outbox = []  # elements ready to dequeue

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        self._transfer()
        return self.outbox.pop()

    def peek(self):
        self._transfer()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox

    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
```

---

## Practice Exercises

### Easy
**E1.** Implement a stack using a single queue.
<details>
<summary>Hint</summary>
On push, enqueue the new element. Then rotate the queue: dequeue and re-enqueue all n-1 previous elements. The new element is now at the front. O(n) push, O(1) pop.
</details>

**E2.** Given the root of a binary tree, return the rightmost node of each level (right side view).

### Medium
**E3.** In a grid with obstacles, find the shortest path from top-left to bottom-right. Return -1 if impossible.
<details>
<summary>Hint</summary>
BFS from source. Each cell is a node; neighbors are the 4 (or 8) adjacent non-obstacle cells.
</details>

**E4.** Given a stream of integers, design a data structure that returns the k-th largest element after each insertion.
<details>
<summary>Hint</summary>
Min-heap of size k. Push each element; if heap size > k, pop. The heap root is always the k-th largest.
</details>

**E5.** Given a list of tasks with cooldown time n, find the minimum number of CPU intervals to finish all tasks.
<details>
<summary>Hint</summary>
Greedy with a priority queue. Always execute the most frequent remaining task. If none available, idle.
</details>

### Hard
**E6.** Find the median of a data stream efficiently. Support `addNum(int num)` and `findMedian()`.
<details>
<summary>Hint</summary>
Two heaps: max-heap for lower half, min-heap for upper half. Balance them after each insertion.
addNum: O(log n), findMedian: O(1).
</details>

---

## Chapter Summary

| Data Structure | Use Case | Key Operation |
|----------------|----------|---------------|
| Queue (deque) | BFS, level-order traversal | O(1) enqueue/dequeue |
| Monotonic Deque | Sliding window max/min | O(n) total |
| Priority Queue | k-th largest, Dijkstra | O(log n) push/pop |
| Two Stacks | Queue simulation | O(1) amortized |

**Previous:** [Chapter 3 → Stacks](03_stacks.md) | **Next:** [Chapter 5 → Hash Tables](05_hash_tables.md)
