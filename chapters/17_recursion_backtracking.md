# Chapter 17: Recursion & Backtracking

> *"Backtracking is 'try a choice, recurse, undo the choice.' It explores the entire space of possibilities."*

---

## 17.1 Why Recursion and Backtracking Matter

**Recursion** solves a problem by solving smaller instances of the same problem (base case + recurrence). **Backtracking** is recursion where you **make a choice**, **recurse**, then **undo the choice** to try the next option — used for permutations, combinations, subsets, N-Queens, Sudoku, and path finding. Interviews love "generate all..." and "find one valid..." problems. Master the **choose → explore → unchoose** template and when to **prune** (early exit when a path can't lead to a solution).

---

## 17.2 Recursion Fundamentals

- **Base case:** When to stop (e.g., empty input, depth reached).
- **Recurrence:** Define result in terms of smaller inputs (e.g., factorial: n * fact(n-1)).
- **Call stack:** Each call gets its own frame; returning pops the frame. Stack overflow when depth is huge — consider iterative or tail recursion (Python doesn't optimize tail calls).

**Example: factorial**

```python
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)
```

**Example: tree height** (see Chapter 6): base case null → 0; else 1 + max(left, right).

---

## 17.3 Backtracking Template

```python
def backtrack(path, options):
    if is_solution(path):
        record(path)
        return
    for choice in options:
        if not valid(choice):
            continue
        path.append(choice)      # choose
        backtrack(path, updated_options)  # explore
        path.pop()               # unchoose
```

**Key:** After exploring with `choice`, remove it so the next iteration tries a different choice. If you pass **copy of state** instead of mutating, you don't need explicit unchoose (but more memory).

---

## 17.4 Permutations (All Orderings)

Generate all permutations of [1..n]. Options at each step: all elements not yet in path.

```python
def permutations(nums):
    out = []
    def bt(path, remaining):
        if not remaining:
            out.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            bt(path, remaining[:i] + remaining[i+1:])
            path.pop()
    bt([], nums)
    return out
```

**With duplicate elements:** Sort first; skip duplicate choices: if `i > 0 and remaining[i] == remaining[i-1]`, skip (when we're building the same prefix again).

---

## 17.5 Combinations (Choose K)

Choose k elements from [1..n]; order doesn't matter. So after picking an element, only consider elements **after** it to avoid (1,2) and (2,1).

```python
def combine(n, k):
    out = []
    def bt(start, path):
        if len(path) == k:
            out.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            bt(i + 1, path)
            path.pop()
    bt(1, [])
    return out
```

---

## 17.6 Subsets (Power Set)

Every element is either in or out. Two choices per element → 2^n subsets.

```python
def subsets(nums):
    out = []
    def bt(i, path):
        if i == len(nums):
            out.append(path[:])
            return
        bt(i + 1, path)           # skip
        path.append(nums[i])
        bt(i + 1, path)           # take
        path.pop()
    bt(0, [])
    return out
```

Or: at each index, iterate from i to end and add each as next element (so each subset is built once).

---

## 17.7 Constraint Satisfaction: N-Queens

Place n queens on n×n so no two attack. Backtrack row by row; for each row, try each column; check no conflict with previous rows (same col, same diagonal: row-col or row+col).

```python
def solve_n_queens(n):
    col = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    board = [['.'] * n for _ in range(n)]
    out = []
    def bt(row):
        if row == n:
            out.append([''.join(r) for r in board])
            return
        for c in range(n):
            if c in col or (row - c) in diag1 or (row + c) in diag2:
                continue
            col.add(c); diag1.add(row - c); diag2.add(row + c)
            board[row][c] = 'Q'
            bt(row + 1)
            board[row][c] = '.'
            col.discard(c); diag1.discard(row - c); diag2.discard(row + c)
    bt(0)
    return out
```

---

## 17.8 Sudoku Solver

Fill empty cells so each row, column, and 3×3 box has 1–9. Backtrack: pick an empty cell, try 1–9, check valid, recurse; if no digit works, return False and backtrack.

---

## 17.9 Pruning

- **Early exit:** If remaining choices can't possibly lead to a solution (e.g., sum already > target), return.
- **Order of choices:** Try "more promising" choices first to find a solution faster (e.g., larger numbers first for combination sum).
- **Memoization:** If the same state can be reached multiple ways and the outcome is the same, memoize (overlaps with DP — Chapter 18).

---

## 17.10 Complexity

Often **exponential** (e.g., O(n!) for permutations, O(2^n) for subsets). Pruning and constraints reduce it in practice.

---

## Practice Exercises

**E1.** Subsets — take/skip per index.

**E2.** Subsets II (with duplicates) — sort, skip duplicate "first of same value" when we already skipped that value.

**E3.** Permutations — backtrack with remaining list or used set.

**E4.** Combination Sum — same number can be used; backtrack with start index and target; prune if target < 0.

**E5.** N-Queens — row by row, check col and diagonals.

**E6.** Sudoku Solver — try 1–9 in empty cell, recurse.

**E7.** Word Search — backtrack on grid; mark visited; unmark on backtrack.

---

## Chapter Summary

| Pattern | Use |
|---------|-----|
| Choose → explore → unchoose | Permutations, combinations, subsets |
| Path + remaining options | Permutations |
| Start index to avoid duplicates | Combinations, combination sum |
| Constraint check each step | N-Queens, Sudoku |
| Pruning | Early exit, order of choices |

**Previous:** [Chapter 16 → Sliding Window](16_sliding_window.md) | **Next:** [Chapter 18 → Dynamic Programming](18_dynamic_programming.md)
