# Chapter 25: B-Trees & B+ Trees

> *"Databases don't use binary search trees. They use B-trees — and for good reason."*

---

## 25.1 Why B-Trees Matter

Binary search trees (and even balanced BSTs like AVL/Red-Black) are designed for **in-memory** data. When data lives on **disk**, each node access can mean a **disk read**. Disk I/O is slow and is done in **blocks** (e.g. 4KB). A B-tree is designed so that **one node fits in one (or a few) disk blocks** and holds **many keys and children** — so one disk read fetches a lot of useful information. That’s why most database indices and file systems use B-trees or their variant **B+ trees**. Understanding them makes you literate in systems and storage.

---

## 25.2 B-Tree Definition

A **B-tree of order m** (or minimum degree t, where m = 2t) is a rooted tree with:

1. **Node capacity:** Every node has at most **m − 1** keys and at most **m** children (except root: at least 2 children if not a leaf).
2. **Root:** The root has at least 1 key (and at least 2 children unless it’s the only node).
3. **Internal nodes:** Every internal node (non-leaf) has at least **⌈m/2⌉ − 1** keys and at least **⌈m/2⌉** children.
4. **Leaves:** All leaves are at the **same depth**.
5. **Ordering:** Keys in each node are sorted; between two keys we have a child subtree containing keys in that range (like a multi-way search tree).

```
Example: B-tree of order 3 (min degree t=2). Each internal node: 1–2 keys, 2–3 children.
Keys in [min, max] per subtree.

         [ 20 ]
        /   |   \
   [5,10]  [25]  [40,50]
   / | \    | \   /  |  \
  L  L  L   L  L  L   L  L   (L = leaf)
```

**Height:** With n keys and minimum degree t, height h ≤ log_t((n+1)/2). So we get **O(log n)** search, but the base of the log is large (e.g. hundreds), so the tree is very shallow and few disk blocks are read.

---

## 25.3 B-Tree Operations (Conceptual)

### Search

Start at root. Compare target with keys in the node; find the range and descend into the corresponding child. Repeat until we hit a leaf or find the key. **Time:** O(log_t n) node accesses = O(log n) with large constant factor (t).

### Insert

1. **Find** the leaf where the key belongs (search).
2. **Insert** the key into that leaf (in sorted order).
3. If the node **overflows** (has m keys): **split** it into two nodes with ⌈m/2⌉ − 1 and ⌈m/2⌉ − 1 keys, and **push the middle key up** to the parent.
4. If the parent overflows, **split recursively** up to the root. If the root splits, create a new root with one key.

**Split example (order 3, max 2 keys per node):** Node [10, 20, 30] overflows → split: left [10], right [30], middle 20 goes to parent.

### Delete

Conceptually: remove the key from a leaf (or from an internal node by replacing with predecessor/successor from a leaf). If a node underflows (too few keys), **borrow** from a sibling or **merge** with a sibling and pull a key down from the parent. Details are more involved; many texts give full deletion rules.

---

## 25.4 B+ Tree

In a **B+ tree**:

- **All keys are duplicated in the leaves** — internal nodes only hold **routing keys** (to guide search).
- **Leaves are linked** in sorted order (singly or doubly linked list).

**Why B+ for databases:**

1. **Range queries:** "All rows with key between A and B" — find the leaf for A, then follow the leaf chain. No need to go back up the tree.
2. **Scan in order:** Traverse the leaf list.
3. **Predictable I/O:** All data lives in leaves; internal nodes are just an index.

```
B+ tree (conceptual):

  Internal:    [ 20 ]              ← routing only
               /     \
  Leaves:  [5,10,15] <-> [20,25,30] <-> [35,40]   ← data + linked list
```

---

## 25.5 B-Tree vs BST / Red-Black

| Aspect | BST / Red-Black | B-Tree |
|--------|------------------|--------|
| Node size | One key (plus children) | Many keys per node |
| Disk | Poor (many small nodes = many I/Os) | Good (one block = one node) |
| Height | O(log₂ n) | O(log_t n), t large |
| Use case | In-memory ordered set/map | Database indices, file systems |

---

## 25.6 Complexity Summary

| Operation | Time (node accesses) | Note |
|-----------|----------------------|------|
| Search | O(log_t n) | t = min degree |
| Insert | O(log_t n) | plus split cost |
| Delete | O(log_t n) | plus merge/borrow |

**Space:** O(n) keys stored; typically each node is one disk block.

---

## Practice Exercises

**E1.** In a B-tree of order 5 (max 4 keys per node), what is the minimum number of keys in an internal node? What is the maximum number of children?

**E2.** Why do B+ trees keep all keys in the leaves and link the leaves? How does that help range scans?

**E3.** (Conceptual) How would you implement a B-tree node in code? What would you store (keys array, children array, leaf flag)?

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| B-tree | Multi-way balanced tree; many keys per node for disk blocks |
| Height | O(log_t n); few disk reads |
| B+ tree | Data only in leaves; leaves linked for range queries |
| Use | Database indices, file systems |

**Previous:** [Chapter 24 → Math & Number Theory](24_math_number_theory.md) | **Next:** [Chapter 26 → Skip List](26_skip_list.md)
