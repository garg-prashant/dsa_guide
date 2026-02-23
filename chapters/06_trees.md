# Chapter 6: Trees (Binary Tree & BST)

> *"Trees are just recursive structures. Every node is the root of its own subtree."*

---

## 6.1 Why Trees Matter

Trees appear everywhere in interviews: binary trees, binary search trees (BST), and tree-shaped recursion. They model hierarchical data (file systems, DOM, org charts) and give you O(log n) search when balanced. Most tree problems reduce to **traversing** (visit every node in some order) or **recursive structure** (solve for left/right subtree, then combine). Mastering traversals and the "pass information up/down" pattern will unlock the majority of tree problems.

---

## 6.2 Tree Terminology

```
            (1)        ← root (depth 0, level 0)
           /   \
         (2)   (3)     ← internal nodes (depth 1)
        / \     \
      (4) (5)   (6)    ← (4),(5) leaves; (6) internal (depth 2)
```

| Term | Definition |
|------|------------|
| **Root** | Top node; no parent |
| **Leaf** | Node with no children |
| **Internal node** | Has at least one child |
| **Depth** | Number of edges from root to this node |
| **Height** | Max depth of any node in the tree (often "height of root") |
| **Balanced** | For every node, heights of left and right subtrees differ by at most 1 (strict) or tree height is O(log n) (loose) |

**Convention:** Height of empty tree = -1; height of single node = 0. Some definitions use 0 for empty and 1 for single node — clarify if needed.

---

## 6.3 Binary Tree Node and Traversals

We'll use a simple node class:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Recursive traversals

**Inorder:** left → root → right. For a BST, inorder gives **sorted order**.

**Preorder:** root → left → right. Used for copying trees and serialization.

**Postorder:** left → right → root. Used when you need children processed before root (e.g., height, delete tree).

**Traversal order on an example tree:**

```
           1
          / \
         2   3
        / \
       4   5
```

| Traversal | Order of visit (node values) |
|-----------|------------------------------|
| **Inorder** (left → root → right) | 4 → 2 → 5 → 1 → 3 |
| **Preorder** (root → left → right) | 1 → 2 → 4 → 5 → 3 |
| **Postorder** (left → right → root) | 4 → 5 → 2 → 3 → 1 |

**How to read inorder:** Start at root; go left until null (visit 4), then root (2), then right subtree (5), then back to root (1), then right (3). So "left subtree, then root, then right subtree" at every node.

```python
def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val)   # process
    inorder(root.right)

def preorder(root):
    if not root:
        return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def postorder(root):
    if not root:
        return
    postorder(root.left)
    postorder(root.right)
    print(root.val)
```

**Time:** O(n), **Space:** O(h) for call stack (h = height; O(n) worst for skewed tree).

---

## 6.4 Iterative Traversals (Stack-Based)

Use an explicit stack to simulate the call stack. Essential when you need to pause/resume or avoid recursion limits.

### Iterative inorder

```python
def inorder_iterative(root):
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        print(node.val)   # process
        node = node.right
```

### Iterative preorder

```python
def preorder_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
```

### Iterative postorder

Postorder is trickier: one approach is to do "reverse preorder" (root → right → left) and reverse the result. Or use a stack with a "visited" flag. Common pattern:

```python
def postorder_iterative(root):
    if not root:
        return []
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]   # reverse = left, right, root
```

---

## 6.5 Level-Order Traversal (BFS)

Process nodes level by level using a queue. See also **Chapter 4 (Queues)** and **Chapter 8 (Graphs)** for BFS.

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    result = []
    while q:
        node = q.popleft()
        result.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return result
```

**Level-by-level (list of lists):**

```python
def level_order_by_level(root):
    if not root:
        return []
    q = deque([root])
    result = []
    while q:
        level_size = len(q)
        level = []
        for _ in range(level_size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result
```

---

## 6.6 Binary Search Tree (BST)

**Invariant:** For every node, all keys in the **left** subtree are **smaller**, and all keys in the **right** subtree are **larger** (or equal, depending on definition).

```
        5
       / \
      3   7
     / \   \
    1   4   9
```

- **Search:** Compare with root; go left if smaller, right if larger. O(h) time.
- **Insert:** Search for the key; when you reach null, insert there. O(h).
- **Delete:** Three cases — (1) leaf: remove; (2) one child: replace with that child; (3) two children: replace with **inorder successor** (smallest in right subtree) or inorder predecessor, then delete that node from its subtree.

```python
def bst_search(root, target):
    while root and root.val != target:
        root = root.left if target < root.val else root.right
    return root

def bst_insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    elif val > root.val:
        root.right = bst_insert(root.right, val)
    return root

def bst_min_node(node):
    while node.left:
        node = node.left
    return node

def bst_delete(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        succ = bst_min_node(root.right)
        root.val = succ.val
        root.right = bst_delete(root.right, succ.val)
    return root
```

---

## 6.7 Why Balanced BSTs Matter

If you insert 1, 2, 3, 4, 5 in order, the BST becomes a **linked list** — height O(n), so search/insert/delete become O(n). **Balanced BSTs** (AVL, Red-Black) keep height O(log n) by rotating after insert/delete. You don't need to implement rotations in interviews, but know:

- **AVL:** Strict balance; heights of left and right differ by at most 1. More rotations, simpler logic.
- **Red-Black:** Relaxed balance; at most 2x the minimum height. Fewer rotations, used in many standard libraries (e.g., `std::map`).

Python's `sorted` containers don't use a balanced BST; for ordered operations you'd use something like `sortedcontainers.SortedList`. For interview problems, assume BST when the problem says "BST" and focus on the invariant and O(h) operations.

---

## 6.8 Tree Serialization and Deserialization

Serialize a tree to a string so you can rebuild it (e.g., for "Serialize and Deserialize Binary Tree"). Common approach: **preorder with null markers**.

```
    1
   / \
  2   3
     /
    4

Preorder with null: "1,2,#,#,3,4,#,#,#"
```

```python
def serialize(root):
    if not root:
        return "#"
    return str(root.val) + "," + serialize(root.left) + "," + serialize(root.right)

def deserialize(data):
    it = iter(data.split(","))
    def build():
        val = next(it, None)
        if val is None or val == "#":
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()
```

---

## 6.9 N-ary (General) Trees

Instead of left/right, a node has a list of children. Same ideas: BFS for level order, DFS (pre/post) for traversal. Often used for file systems, org charts, or "design" problems.

```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def nary_preorder(root):
    if not root:
        return []
    out = [root.val]
    for child in root.children:
        out += nary_preorder(child)
    return out
```

---

## 6.10 Common Patterns

### Maximum depth (height)

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Diameter (longest path between any two nodes)

The **diameter** is the longest path between any two nodes (number of edges). That path either goes **through** some node or stays entirely in a subtree. For each node, the longest path **through** that node has length = (left height) + (right height) — we don't add 1 for the node if we count edges. Take the maximum over all nodes.

**Example:** In the tree below, the diameter is 4 (path 4–2–1–3–6 or 5–2–1–3–6). At node 1, left height = 2, right height = 2, so through 1 we get 2+2 = 4.

```
           1
          / \
         2   3
        / \   \
       4   5   6
```

```python
def diameter_of_binary_tree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        L = height(node.left)
        R = height(node.right)
        best = max(best, L + R)
        return 1 + max(L, R)
    height(root)
    return best
```

### Lowest common ancestor (LCA)

The **lowest common ancestor** of two nodes p and q is the deepest node that has both p and q as descendants (a node can be a descendant of itself).

**Example:** In the tree above, LCA(4, 5) = 2, LCA(4, 6) = 1, LCA(2, 2) = 2.

For a **binary tree** (not necessarily BST): if the current node is p or q or null, return it. Recurse on left and right. If **both** sides return a non-null node, the current node is the LCA. Otherwise return whichever side is non-null (the LCA is in that subtree).

```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

### Validate BST

Pass a (min_allowed, max_allowed) range down. Update range when going left (max = root.val) or right (min = root.val).

```python
def is_valid_bst(root, lo=float("-inf"), hi=float("inf")):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)
```

---

## 6.11 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| All traversals (n nodes) | O(n) | O(h) recursive; O(n) iterative stack/queue |
| BST search / insert / delete | O(h) | O(h) recursive |
| Balanced BST (h = O(log n)) | O(log n) | O(log n) |
| Serialize / deserialize | O(n) | O(n) |

---

## 6.12 Interview Gotchas

- **Null checks:** Always handle `root is None` and `node.left` / `node.right` before using.
- **BST invariant:** Use strict &lt; and &gt; unless the problem allows duplicates; then define left vs right consistently.
- **Global / nonlocal:** For "max over all nodes" (e.g., diameter), use a variable outside the recursion or return extra info (e.g., height + best diameter in subtree).
- **Inorder in BST:** Inorder gives sorted order — use for "kth smallest", "validate BST", or two-pointer in BST.

---

## Practice Exercises

### Easy

**E1.** Maximum Depth of Binary Tree — return the height of the tree.

<details><summary>Hint</summary>
Base case: null → 0. Else 1 + max(left_height, right_height).
</details>

**E2.** Same Tree — given two roots, check if the two trees are identical.

<details><summary>Hint</summary>
Both null → true; one null → false; else compare val and recurse on left and right.
</details>

**E3.** Invert Binary Tree — swap left and right for every node.

<details><summary>Hint</summary>
Postorder: invert left and right subtrees, then swap root.left and root.right.
</details>

### Medium

**E4.** Binary Tree Level Order Traversal — return values level by level (list of lists).

<details><summary>Hint</summary>
BFS with a queue; each iteration processes one level (current queue length).
</details>

**E5.** Lowest Common Ancestor of a Binary Tree (non-BST).

<details><summary>Hint</summary>
If root is p or q or null, return root. Recurse left and right. If both return non-null, root is LCA; else return whichever side is non-null.
</details>

**E6.** Kth Smallest Element in a BST.

<details><summary>Hint</summary>
Inorder traversal; count nodes. When count reaches k, return that node's value. Or use iterative inorder and stop at k.
</details>

**E7.** Validate Binary Search Tree.

<details><summary>Hint</summary>
Pass (min, max) down; for left subtree max = root.val, for right min = root.val.
</details>

### Hard

**E8.** Serialize and Deserialize Binary Tree.

<details><summary>Hint</summary>
Preorder with "#" for nulls; deserialize by consuming the same preorder sequence recursively.
</details>

**E9.** Binary Tree Maximum Path Sum — path = any sequence of connected nodes; at most one turn (path need not pass root).

<details><summary>Hint</summary>
For each node, max path "through" node = node.val + max(0, left_gain) + max(0, right_gain). Return upward only one branch: node.val + max(left_gain, right_gain). Keep a global max.
</details>

---

## Chapter Summary

| Pattern | Use Case |
|---------|----------|
| Inorder (BST) | Sorted order, kth smallest, validate BST |
| Preorder | Serialization, copy tree |
| Postorder | Height, diameter, delete, when children first |
| Level-order (BFS) | Level-by-level, shortest path in tree |
| LCA | Common ancestor of two nodes |
| Range (min, max) | Validate BST, range queries in BST |

**Previous:** [Chapter 5 → Hash Tables](05_hash_tables.md) | **Next:** [Chapter 7 → Heaps](07_heaps.md)
