# The Complete DSA Handbook
## A FAANG Interview Preparation Guide — Python Edition

---

> *"An algorithm must be seen to be believed."* — Donald Knuth

---

## About This Book

This handbook is a structured, end-to-end guide to Data Structures and Algorithms for software engineering interviews at top technology companies. Every chapter teaches one concept through:

- **Conceptual explanation** — the *why*, not just the *how*
- **Worked examples** — tracing through algorithms by hand
- **Python implementations** — clean, interview-ready code
- **Complexity analysis** — time and space for every solution
- **Practice exercises** — graded Easy / Medium / Hard

Read chapters in order. Each one builds on the last.

---

## Table of Contents

### Part I — Foundations
| Chapter | Topic | File |
|---------|-------|------|
| 00 | Complexity Analysis — Big O, Time, Space | [00_complexity.md](chapters/00_complexity.md) |

### Part II — Data Structures
| Chapter | Topic | File |
|---------|-------|------|
| 01 | Arrays & Strings | [01_arrays_strings.md](chapters/01_arrays_strings.md) |
| 02 | Linked Lists | [02_linked_lists.md](chapters/02_linked_lists.md) |
| 03 | Stacks | [03_stacks.md](chapters/03_stacks.md) |
| 04 | Queues & Deques | [04_queues.md](chapters/04_queues.md) |
| 05 | Hash Tables | [05_hash_tables.md](chapters/05_hash_tables.md) |
| 06 | Trees — Binary Tree & BST | [06_trees.md](chapters/06_trees.md) |
| 07 | Heaps & Priority Queues | [07_heaps.md](chapters/07_heaps.md) |
| 08 | Graphs | [08_graphs.md](chapters/08_graphs.md) |
| 09 | Tries | [09_tries.md](chapters/09_tries.md) |
| 10 | Union-Find (Disjoint Set Union) | [10_union_find.md](chapters/10_union_find.md) |
| 11 | Segment Trees | [11_segment_trees.md](chapters/11_segment_trees.md) |
| 12 | Fenwick Trees (Binary Indexed Trees) | [12_fenwick_trees.md](chapters/12_fenwick_trees.md) |

### Part III — Algorithms
| Chapter | Topic | File |
|---------|-------|------|
| 13 | Sorting Algorithms | [13_sorting.md](chapters/13_sorting.md) |
| 14 | Binary Search | [14_binary_search.md](chapters/14_binary_search.md) |
| 15 | Two Pointers | [15_two_pointers.md](chapters/15_two_pointers.md) |
| 16 | Sliding Window | [16_sliding_window.md](chapters/16_sliding_window.md) |
| 17 | Recursion & Backtracking | [17_recursion_backtracking.md](chapters/17_recursion_backtracking.md) |
| 18 | Dynamic Programming | [18_dynamic_programming.md](chapters/18_dynamic_programming.md) |
| 19 | Greedy Algorithms | [19_greedy.md](chapters/19_greedy.md) |
| 20 | Divide & Conquer | [20_divide_and_conquer.md](chapters/20_divide_and_conquer.md) |
| 21 | Graph Algorithms (Dijkstra, MST, Topo Sort) | [21_graph_algorithms.md](chapters/21_graph_algorithms.md) |
| 22 | String Algorithms (KMP, Rabin-Karp) | [22_string_algorithms.md](chapters/22_string_algorithms.md) |
| 23 | Bit Manipulation | [23_bit_manipulation.md](chapters/23_bit_manipulation.md) |
| 24 | Math & Number Theory | [24_math_number_theory.md](chapters/24_math_number_theory.md) |

### Part IV — Advanced (Expert Level)
| Chapter | Topic | File |
|---------|-------|------|
| 25 | B-Trees & B+ Trees | [25_btrees.md](chapters/25_btrees.md) |
| 26 | Skip List | [26_skip_list.md](chapters/26_skip_list.md) |
| 27 | Reservoir Sampling & Randomized Algorithms | [27_reservoir_sampling.md](chapters/27_reservoir_sampling.md) |
| 28 | Sweep Line | [28_sweep_line.md](chapters/28_sweep_line.md) |
| 29 | Suffix Array & Suffix Tree | [29_suffix_array_tree.md](chapters/29_suffix_array_tree.md) |
| 30 | Advanced Graph Algorithms | [30_advanced_graphs.md](chapters/30_advanced_graphs.md) |
| 31 | Advanced DP & Query Optimization | [31_advanced_dp.md](chapters/31_advanced_dp.md) |

---

## 12-Week Study Plan

### Phase 1 — Core Data Structures (Weeks 1–4)
| Week | Monday–Wednesday | Thursday–Friday | Weekend |
|------|-----------------|-----------------|---------|
| 1 | Ch 00: Complexity + Ch 01: Arrays | Ch 02: Linked Lists | Solve 10 Easy problems |
| 2 | Ch 03: Stacks + Ch 04: Queues | Ch 05: Hash Tables | Solve 10 Easy/Medium |
| 3 | Ch 06: Trees (BFS/DFS) | Ch 07: Heaps | Mock interview |
| 4 | Ch 08: Graphs + Ch 09: Tries | Ch 10: Union-Find | Solve 15 Medium |

### Phase 2 — Algorithms (Weeks 5–9)
| Week | Focus | Target |
|------|-------|--------|
| 5 | Sorting + Binary Search (Ch 13–14) | 15 problems |
| 6 | Two Pointers + Sliding Window (Ch 15–16) | 15 problems |
| 7 | Recursion + Backtracking (Ch 17) | 10 problems |
| 8 | Dynamic Programming 1D (Ch 18) | 15 problems |
| 9 | Dynamic Programming 2D + Advanced | 10 problems |

### Phase 3 — Advanced & Review (Weeks 10–12)
| Week | Focus | Target |
|------|-------|--------|
| 10 | Graph Algorithms + Greedy (Ch 19, 21) | 15 problems |
| 11 | Advanced: Segment Trees, BIT, Bit Manip, Math (Ch 11–12, 23–24) | 10 problems |
| 12 | Full mock interviews, review weak areas | 3 mock interviews |

### Phase 4 — Expert (Optional, after core is solid)
| Week | Focus | Target |
|------|-------|--------|
| 13+ | Part IV: B-Trees, Skip List, Reservoir Sampling (Ch 25–27) | Deep understanding |
| 14+ | Sweep Line, Suffix Array/Tree (Ch 28–29) | 5–10 problems |
| 15+ | Advanced Graphs, Advanced DP (Ch 30–31) | 10 problems |

---

## Interview Strategy

### The 7-Step Framework

```
1. LISTEN   — Ask clarifying questions. Never assume.
2. EXAMPLE  — Draw 2–3 examples, including edge cases.
3. BRUTE    — State the brute force. Never skip this.
4. OPTIMIZE — Identify bottleneck. Apply patterns.
5. WALKTHROUGH — Trace your algorithm before coding.
6. CODE     — Write clean code. Talk while you type.
7. TEST     — Test with your examples. Find bugs yourself.
```

### Pattern Recognition Cheat Sheet

| Problem Signal | Pattern to Try |
|----------------|---------------|
| Sorted array, find pair | Two Pointers |
| Substring with constraint | Sliding Window |
| Find cycle in list/graph | Fast & Slow Pointers |
| Sorted array, find value | Binary Search |
| Shortest path (unweighted) | BFS |
| All paths / combinations | DFS + Backtracking |
| Optimal substructure + overlapping subproblems | Dynamic Programming |
| Locally optimal = globally optimal | Greedy |
| Connected components, cycle in undirected graph | Union-Find |
| Word problems, prefix matching | Trie |
| Range sum/min/max queries | Segment Tree or BIT |
| Next greater/smaller element | Monotonic Stack |
| k largest/smallest elements | Heap |

### Complexity Quick Reference

| Complexity | Name | Example | n=10⁶ (approx) |
|------------|------|---------|-----------------|
| O(1) | Constant | Array access | instant |
| O(log n) | Logarithmic | Binary search | ~20 ops |
| O(n) | Linear | Linear scan | 10⁶ ops |
| O(n log n) | Linearithmic | Merge sort | ~2×10⁷ ops |
| O(n²) | Quadratic | Nested loops | 10¹² ops ❌ |
| O(2ⁿ) | Exponential | Brute force subsets | ∞ ❌ |

> **Rule of thumb:** For n = 10⁵, you need O(n log n) or better.
> For n = 10³, O(n²) is acceptable.

---

## Running the Code

All code examples can be run directly:

```bash
# Run a specific chapter's examples
python chapters/implementations/01_arrays.py

# Or open in Jupyter for interactive exploration
jupyter notebook
```

Each chapter has a corresponding implementation file in `chapters/implementations/`.
