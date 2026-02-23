# Chapter 31: Advanced DP & Query Optimization

> *"Digit DP, convex hull trick, and Mo's algorithm — when standard DP and segment trees aren't enough."*

---

## 31.1 Why These Topics Matter

**Chapter 18** covered classic 1D/2D DP. Here we add **digit DP** (counting numbers with a property over a range), the **convex hull trick** (optimizing certain recurrences with lines), and **Mo's algorithm** (offline range queries in O(n√n)). These appear in competitive programming and hard interviews. They round out an expert-level toolkit.

---

## 31.2 Digit DP

**Pattern:** Count integers in [L, R] (or 0..N) that satisfy a property (e.g. no digit 4, sum of digits = S, number has a substring "13"). We **walk the digits** of the number (left to right) and keep **state**: position, tight (whether we're still bounded by the input), and problem-specific state (e.g. digit sum, last digit, flag for "already had 13").

**Example:** Count numbers in [0, N] where no digit is 4.

**State:** dp[pos][tight] = count of ways to fill from pos onward; tight = 1 means we must not exceed N so far. At each position, try digits 0..upper (upper = N[pos] if tight else 9); skip 4; update tight.

```python
def count_without_digit_4(N_str):
    """Count numbers in [0, N] (N given as string) with no digit 4."""
    n = len(N_str)
    N = list(map(int, N_str))

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(pos, tight):
        if pos == n:
            return 1
        upper = N[pos] if tight else 9
        total = 0
        for d in range(upper + 1):
            if d == 4:
                continue
            new_tight = tight and (d == upper)
            total += dp(pos + 1, new_tight)
        return total

    return dp(0, True)
```

**Time:** O(digits × 2) = O(log N) states; often other state dimensions (e.g. digit sum) add factors.

---

## 31.3 Convex Hull Trick (Line Container)

**Setting:** Recurrence of the form dp[i] = min over j of (m[j]*x[i] + c[j]) + const. We can think of each j as a **line** y = m[j]*x + c[j]. For a given x[i], we want the **minimum** value among these lines at x = x[i]. So we maintain the **lower envelope** of lines (convex hull of lines when we want minimum).

**Idea:** Add lines in order of slope (e.g. increasing m). Keep a stack or deque of lines that form the lower envelope. When adding a new line, pop lines that are never minimal (because the new line dominates them). Query at x: binary search to find which segment of the envelope is active at x (or use a dynamic structure).

**Simplified (lines added in order of slope, queries in order of x):** Use a deque; at query x, pop from front while the next line gives a smaller value at x; then the front line is optimal. **Time:** O(n) for n lines and n queries if both are ordered.

**Use case:** DP like dp[i] = min_j (a[j]*b[i] + dp[j]) with suitable monotonicity.

---

## 31.4 Mo's Algorithm (Offline Range Queries)

**Problem:** Many queries [L, R] over an array; each query asks for something we can update incrementally (e.g. count of distinct elements, frequency-based value). **Offline:** we can reorder queries.

**Idea:** Sort queries by **block of L** (L divided by √n), and within a block by R. Use two pointers (current L, R) and expand/shrink the window to the next query; each move is O(1) update. **Total moves:** L moves O(Q √n) (each query can move L by O(√n)), R moves O(n √n) (R only increases within a block). So **total O((n + Q) √n)**.

**Requirements:** (1) Answer for [L, R] can be updated from [L±1, R] or [L, R±1] in O(1). (2) Queries are offline.

```python
def mo_algorithm(arr, queries):
    """queries: list of (l, r). Returns list of answers (e.g. distinct count)."""
    n = len(arr)
    block_sz = int(n ** 0.5) + 1

    def key(q):
        i, (l, r) = q
        b = l // block_sz
        return (b, r if b % 2 == 0 else -r)

    Q = [(i, q) for i, q in enumerate(queries)]
    Q.sort(key=key)

    # Implement: add(i), remove(i), get_answer() with global L, R and a freq counter
    # For "count distinct": freq[x], and count of x with freq[x]>0
    freq = {}
    distinct = 0

    def add(i):
        nonlocal distinct
        x = arr[i]
        freq[x] = freq.get(x, 0) + 1
        if freq[x] == 1:
            distinct += 1

    def remove(i):
        nonlocal distinct
        x = arr[i]
        freq[x] -= 1
        if freq[x] == 0:
            distinct -= 1

    L, R = 0, -1
    ans = [0] * len(queries)
    for i, (l, r) in Q:
        while R < r:
            R += 1
            add(R)
        while R > r:
            remove(R)
            R -= 1
        while L < l:
            remove(L)
            L += 1
        while L > l:
            L -= 1
            add(L)
        ans[i] = distinct  # or get_answer()
    return ans
```

---

## 31.5 Persistent Segment Tree (Brief)

A **persistent** data structure keeps all **versions** after updates. **Persistent segment tree:** Each update creates a new root and O(log n) new nodes; old version remains. So we can query "range [L,R] at time t". Used for "kth smallest in range" (binary search + persistent segment tree by value). Implementation is heavier; often used in advanced problems.

---

## 31.6 When to Use Which

| Problem type | Technique |
|--------------|-----------|
| Count numbers in [L,R] with digit property | Digit DP |
| dp[i] = min_j (line in j at x[i]) | Convex hull trick |
| Offline range queries, O(1) add/remove element | Mo's algorithm |
| Query past versions of a segment tree | Persistent segment tree |

---

## Practice Exercises

**E1.** (Digit DP) Count numbers in [1, N] that contain the substring "13". State: pos, tight, found_13 (bool).

**E2.** (Convex hull) Given lines (m, c), process queries "min over all lines at x = q". Assume lines added in order of slope; use a deque for the envelope.

**E3.** (Mo's) Given an array and Q queries [L, R], return the count of distinct elements in each range. Use Mo's with a frequency map.

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Digit DP | Walk digits; state = position, tight, + problem state |
| Convex hull trick | Lower envelope of lines; min at x; deque when ordered |
| Mo's algorithm | Offline range queries; sort by (L/√n, R); O((n+Q)√n) |
| Persistent ST | Keep all versions; O(log n) per update, query any version |

**Previous:** [Chapter 30 → Advanced Graph Algorithms](30_advanced_graphs.md)  
**Part IV complete.** For the full index, see [README](../README.md).
