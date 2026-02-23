# DSA Handbook — Guide Overview

This document describes the **DSA Handbook**: what it is, who it’s for, how it’s organized, and what each chapter covers.

---

## Purpose

The handbook is an **exhaustive Data Structures and Algorithms guide** for technical interview preparation (e.g. FAANG and similar). It is designed so that, once completed, **no other study material is required** for core DSA topics. Each chapter includes concepts, Python implementations, complexity analysis, pattern recognition, and practice problems (Easy / Medium / Hard) with hints.

---

## Contents

The guide has **32 chapters** in four parts. Chapters live in the `chapters/` directory. Parts I–III cover core interview DSA; **Part IV (Advanced)** is for readers who want expert-level depth.

### Part I — Foundations (Chapters 00–05)

| Chapter | Topic | File |
|---------|--------|------|
| 00 | Complexity Analysis — Big O, time, space | `chapters/00_complexity.md` |
| 01 | Arrays & Strings | `chapters/01_arrays_strings.md` |
| 02 | Linked Lists | `chapters/02_linked_lists.md` |
| 03 | Stacks | `chapters/03_stacks.md` |
| 04 | Queues & Deques | `chapters/04_queues.md` |
| 05 | Hash Tables | `chapters/05_hash_tables.md` |

### Part II — Data Structures (Chapters 06–12)

| Chapter | Topic | File |
|---------|--------|------|
| 06 | Trees (Binary Tree & BST) | `chapters/06_trees.md` |
| 07 | Heaps & Priority Queues | `chapters/07_heaps.md` |
| 08 | Graphs | `chapters/08_graphs.md` |
| 09 | Tries | `chapters/09_tries.md` |
| 10 | Union-Find (Disjoint Set Union) | `chapters/10_union_find.md` |
| 11 | Segment Trees | `chapters/11_segment_trees.md` |
| 12 | Fenwick Trees (Binary Indexed Trees) | `chapters/12_fenwick_trees.md` |

### Part III — Algorithms (Chapters 13–24)

| Chapter | Topic | File |
|---------|--------|------|
| 13 | Sorting Algorithms | `chapters/13_sorting.md` |
| 14 | Binary Search | `chapters/14_binary_search.md` |
| 15 | Two Pointers | `chapters/15_two_pointers.md` |
| 16 | Sliding Window | `chapters/16_sliding_window.md` |
| 17 | Recursion & Backtracking | `chapters/17_recursion_backtracking.md` |
| 18 | Dynamic Programming | `chapters/18_dynamic_programming.md` |
| 19 | Greedy Algorithms | `chapters/19_greedy.md` |
| 20 | Divide & Conquer | `chapters/20_divide_and_conquer.md` |
| 21 | Graph Algorithms | `chapters/21_graph_algorithms.md` |
| 22 | String Algorithms | `chapters/22_string_algorithms.md` |
| 23 | Bit Manipulation | `chapters/23_bit_manipulation.md` |
| 24 | Math & Number Theory | `chapters/24_math_number_theory.md` |

### Part IV — Advanced (Chapters 25–31)

| Chapter | Topic | File |
|---------|--------|------|
| 25 | B-Trees & B+ Trees | `chapters/25_btrees.md` |
| 26 | Skip List | `chapters/26_skip_list.md` |
| 27 | Reservoir Sampling & Randomized Algorithms | `chapters/27_reservoir_sampling.md` |
| 28 | Sweep Line | `chapters/28_sweep_line.md` |
| 29 | Suffix Array & Suffix Tree | `chapters/29_suffix_array_tree.md` |
| 30 | Advanced Graph Algorithms | `chapters/30_advanced_graphs.md` |
| 31 | Advanced DP & Query Optimization | `chapters/31_advanced_dp.md` |

---

## What Each Chapter Covers

### Part II — Data Structures (06–12)

**06 — Trees**  
Terminology (root, leaf, height, depth, balanced). Binary traversals: inorder, preorder, postorder (recursive and iterative). Level-order (BFS). BST: invariant, insert, delete, search. Balanced BST (AVL/Red-Black at a high level). Tree serialization/deserialization. N-ary trees (brief). Patterns: lowest common ancestor, diameter, max depth.

**07 — Heaps**  
Heap property (min-heap, max-heap). Heapify up/down. Python `heapq` (min-heap, max-heap trick). Applications: k-largest, merge k sorted lists, median of stream. Heap sort.

**08 — Graphs**  
Representations: adjacency list vs matrix. Directed/undirected, weighted/unweighted. BFS (unweighted shortest path). Multisource BFS, 0/1 BFS (mention). DFS: cycle detection, topological sort. Connected components. Common interview patterns.

**09 — Tries**  
Node structure. Insert, search, startsWith. Trade-offs vs hash maps. Applications: autocomplete, word search, IP routing. Compressed tries (brief).

**10 — Union-Find**  
Naive union-find. Path compression and union by rank/size. Amortized complexity. Applications: number of islands, cycle detection, Kruskal’s MST.

**11 — Segment Trees**  
When to use (range queries + point/range updates). Build, point update, range query (sum/min/max). Lazy propagation. Comparison with Fenwick tree.

**12 — Fenwick Trees**  
Prefix-sum motivation. Lowbit trick. Point update, prefix query. Difference-array technique for range updates. 2D Fenwick (brief).

### Part III — Algorithms (13–24)

**13 — Sorting**  
Bubble, selection, insertion (O(n²)). Merge sort, quick sort, heap sort. Counting sort, radix sort. Stability and in-place trade-offs. Python `sort()` / `sorted()` (Timsort).

**14 — Binary Search**  
Classic template. Lower/upper bound. Rotated array, 2D matrix. Binary search on the answer. Common pitfalls.

**15 — Two Pointers**  
Opposite ends (two-sum, trapping rain water). Same direction (remove duplicates). Fast & slow (Floyd cycle). Three-sum, four-sum. Two pointers vs sliding window.

**16 — Sliding Window**  
Fixed- and variable-size windows. Frequency map. Longest substring without repeats, minimum window substring. Deque-based max/min in window.

**17 — Recursion & Backtracking**  
Base case, recurrence, call stack. Backtracking template (choose → explore → unchoose). Permutations, combinations, subsets. N-Queens, Sudoku. Pruning.

**18 — Dynamic Programming**  
Optimal substructure and overlapping subproblems. Top-down (memoization) vs bottom-up (tabulation). 1D: Fibonacci, stairs, house robber, coin change. 2D: LCS, edit distance, 0/1 knapsack. DP on strings, intervals, trees (brief). How to spot DP.

**19 — Greedy**  
Greedy choice property and optimal substructure. Proving correctness (exchange argument). Activity selection, intervals: merge, insert, meeting rooms. Jump game. Huffman (conceptual). When greedy fails (e.g. coin change).

**20 — Divide & Conquer**  
Divide, conquer, combine. Master theorem. Merge sort and quick sort in this lens. Quick select. Binary search as D&C. Strassen (conceptual).

**21 — Graph Algorithms**  
Dijkstra (single-source, non-negative). Bellman-Ford (negative weights, cycles). Floyd-Warshall (all-pairs). MST: Prim, Kruskal. Topological sort (Kahn, DFS). Strongly connected components (Kosaraju, brief). Bidirectional BFS. A* (conceptual).

**22 — String Algorithms**  
Naive matching. KMP (failure function, linear search). Rabin-Karp (rolling hash). Z-algorithm. Manacher (longest palindromic substring). When to use which.

**23 — Bit Manipulation**  
Bitwise operators. Check/set/clear/toggle bits. XOR properties. Power-of-2 check. Single number, missing number. Subsets via bitmasks. Signed/unsigned, overflow.

**24 — Math & Number Theory**  
Euclidean GCD, extended Euclidean (modular inverse). Modular arithmetic and exponentiation. Primes: trial division, Sieve of Eratosthenes. Combinatorics: factorial, nCr (with/without mod). Problems: count primes, power of three, happy number, trailing zeroes.

---

## How Each Chapter Is Structured

Every chapter follows the same pattern:

1. **Opening quote**
2. **Why this topic matters** (1–2 paragraphs)
3. **Core concepts** with explanations and, where useful, ASCII diagrams
4. **Python code** (clean, commented)
5. **Complexity** (time and space in tables)
6. **Interview patterns and gotchas**
7. **Practice problems** — Easy / Medium / Hard, with LeetCode-style names or descriptions and hints

Chapters cross-reference each other (e.g. DFS in trees and recursion, monotonic stack in Stacks) so the guide stays self-contained.

---

## Recommended Reading Order

Read **sequentially from 00 through 24** for core interview prep. Later chapters assume earlier ones (e.g. graphs before graph algorithms, sorting before binary-search variants). Part I (00–05) is the foundation; Part II builds data structures; Part III applies and combines them.

**Part IV (25–31)** is optional and advanced. Tackle it after mastering Parts I–III. It assumes comfort with graphs (Ch 8, 21), strings (Ch 22), segment trees (Ch 11), and DP (Ch 18).

---

## Cross-References Within the Guide

Some ideas appear first in earlier chapters; later chapters refer back instead of repeating:

- **Ch 01:** Prefix sums, two pointers, sliding window basics  
- **Ch 03:** Monotonic stack (next greater/smaller, largest rectangle in histogram)  
- **Ch 04:** Monotonic deque (sliding window max/min)  
- **Ch 05:** LRU Cache (hash map + doubly linked list)

---

## Part IV — Advanced (Chapters 25–31) — What Each Covers

**25 — B-Trees & B+ Trees**  
Why databases use B-trees (disk I/O, block size). Node structure (many keys/children). Insert, split, merge. B+ tree: leaves linked for range scans; data only in leaves. Comparison with BST/red-black.

**26 — Skip List**  
Probabilistic alternative to balanced trees. Multiple levels of linked lists; expected O(log n) search/insert/delete. Insert by random level. Implementation and expected height.

**27 — Reservoir Sampling & Randomized Algorithms**  
Uniform random sample of size k from a stream of unknown size. Proof of correctness. Applications: streaming, big data. Other randomized ideas: randomized quicksort, hash-based sampling.

**28 — Sweep Line**  
Sweep a line across the plane; maintain invariants at events. Interval overlap, merging intervals, rectangle area union, closest pair (conceptual). Event ordering and data structures (e.g. segment tree or BST for active intervals).

**29 — Suffix Array & Suffix Tree**  
Suffix array: sort all suffixes; LCP array. Substring search, LCS of two strings. Suffix tree: trie of all suffixes; Ukkonen (conceptual). When to use which.

**30 — Advanced Graph Algorithms**  
Bridges and articulation points (DFS tree, low link). Strongly connected components (Tarjan, Kosaraju). Max flow: Ford-Fulkerson, Edmonds-Karp, min-cut. Bipartite matching (conceptual).

**31 — Advanced DP & Query Optimization**  
Digit DP (count numbers with property). Convex hull trick (line container for DP). Mo's algorithm (offline range queries in O(n√n)). Persistent segment tree (brief). When to use which pattern.
