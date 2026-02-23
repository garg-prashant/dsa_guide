# Chapter 26: Skip List

> *"A skip list is a probabilistic balanced structure. No rotations — just random levels."*

---

## 26.1 Why Skip Lists Matter

Balanced BSTs (AVL, Red-Black) give O(log n) search and update but require **rotations** and careful rebalancing. A **skip list** achieves **expected** O(log n) search, insert, and delete **without rotations** — structure is maintained by **random choice** of node "height." It's easier to implement than a balanced BST and appears in real systems (e.g. Redis sorted sets use a variant). It also illustrates how **randomization** can simplify algorithms.

---

## 26.2 Structure

A skip list is built from **sorted linked lists** arranged in **layers**. The bottom layer (level 0) is the full sorted list. Each node appears in level 0; with probability (e.g. 1/2) it also appears in level 1; with probability 1/2 again it appears in level 2; and so on. So we get multiple "express lanes": higher levels have fewer nodes and let us skip large stretches.

```
Level 2:    1 --------------------------> 9
Level 1:    1 --------> 5 --------> 9
Level 0:    1 -> 3 -> 5 -> 7 -> 9

Search for 7: Start at 1 (L2), go right to 9 (too far), drop to L1, go to 5, then L0 to 7.
```

**Invariant:** Each level is a subset of the level below, sorted. The top level has O(log n) nodes in expectation.

---

## 26.3 Operations

### Search

Start at the **head** of the top level. Move **right** while the next key is ≤ target. When the next key is > target, **drop down** one level. Repeat until we reach level 0 and find the node or pass it. **Expected time:** O(log n).

### Insert

1. **Search** for the position (we get the predecessors at each level).
2. Create a new node. Its level is chosen **randomly**: level 0 with probability 1, level 1 with probability 1/2, level 2 with 1/4, etc. (e.g. flip a coin until tails).
3. **Splice** the new node into the list at each level from 0 up to its level, using the predecessors found during search.

### Delete

Search for the node; at each level where it appears, unlink it from the list. **Expected time:** O(log n).

---

## 26.4 Random Level

Common approach: **geometric distribution**. Start at level 0; while random() < p (e.g. p = 0.5), increment level. Max level is often capped (e.g. 32) to avoid rare very high towers.

```python
import random

def random_level(p=0.5, max_level=32):
    level = 0
    while random.random() < p and level < max_level:
        level += 1
    return level
```

**Expected number of levels for a node:** 1/(1−p). For p=1/2, expected ≈ 2. So total expected space is O(n).

---

## 26.5 Implementation Sketch

```python
class SkipNode:
    def __init__(self, val, level):
        self.val = val
        self.forward = [None] * (level + 1)  # forward[i] = next at level i

class SkipList:
    def __init__(self, p=0.5, max_level=32):
        self.p = p
        self.max_level = max_level
        self.head = SkipNode(float('-inf'), max_level)
        self.level = 0  # current max level in use

    def _random_level(self):
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def search(self, target):
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < target:
                curr = curr.forward[i]
        curr = curr.forward[0]
        return curr and curr.val == target

    def add(self, val):
        update = [None] * (self.max_level + 1)
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].val < val:
                curr = curr.forward[i]
            update[i] = curr
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl
        node = SkipNode(val, lvl)
        for i in range(lvl + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
```

---

## 26.6 Complexity

| Operation | Expected Time | Expected Space |
|-----------|----------------|----------------|
| Search | O(log n) | O(n) for n nodes |
| Insert | O(log n) | O(log n) new pointers |
| Delete | O(log n) | — |

**Worst case:** O(n) if the random levels are unlucky; with a cap on max level and p=1/2, worst case is very rare and still bounded.

---

## Practice Exercises

**E1.** In a skip list with p = 1/2, what is the expected number of nodes at level 1? At level k?

**E2.** Implement `delete(val)` for the skip list sketch above.

**E3.** How would you implement "find the kth smallest element" in a skip list? (Hint: store "width" or "span" at each pointer.)

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Structure | Sorted lists at multiple levels; random level per node |
| Search | Move right then drop down; O(log n) expected |
| Insert/Delete | Random level + splice; no rotations |
| Use | Simpler than balanced BST; used in Redis etc. |

**Previous:** [Chapter 25 → B-Trees](25_btrees.md) | **Next:** [Chapter 27 → Reservoir Sampling](27_reservoir_sampling.md)
