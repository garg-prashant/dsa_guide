# Chapter 18: Dynamic Programming

> *"DP is recursion with memory. If subproblems repeat, remember the answer and reuse it."*

---

## 18.1 Why DP Matters

**Dynamic programming** solves problems with **overlapping subproblems** and **optimal substructure**: the best solution is built from best solutions of smaller subproblems. You implement it either **top-down** (memoized recursion) or **bottom-up** (table filled in order). Interviews ask 1D (Fibonacci, stairs, house robber, coin change), 2D (LCS, edit distance, knapsack), and sometimes DP on strings, intervals, or trees. Recognizing "recurrence + overlapping subproblems" is the first step.

---

## 18.2 When to Use DP

- **Optimal substructure:** Optimal answer depends on optimal answers to smaller instances (e.g., max profit up to day i depends on day i-1).
- **Overlapping subproblems:** Same subproblem is solved many times (e.g., fib(n-2) used by both fib(n-1) and fib(n)).
- **Ask for:** "minimum/maximum", "number of ways", "is it possible" over sequences/choices.

### Overlapping Subproblems: Fibonacci Call Tree

Naive recursion recomputes the same values repeatedly:

```
                    fib(5)
                   /      \
              fib(4)      fib(3)
              /    \      /    \
         fib(3)  fib(2) fib(2) fib(1)
         /  \    /  \   /  \
    fib(2) f(1) f(1)f(0) ...
     /  \
 fib(1) fib(0)
```

`fib(3)` and `fib(2)` appear multiple times. **Memoization** or **tabulation** ensures each subproblem is solved only once.

---

## 18.3 Top-Down (Memoization)

Write the recurrence as recursion; **cache** results so each state is computed once. When you need `dp(i)`, check the cache first; if missing, compute and store.

```python
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

---

## 18.4 Bottom-Up (Tabulation)

Fill a table in an order that **respects dependencies**: when you compute `dp[i]`, all values it depends on (e.g. `dp[i-1]`, `dp[i-2]`) must already be filled. Saves stack space and often easier to analyze.

### Worked Example: Fibonacci Table (n = 5)

**State:** `dp[i]` = Fibonacci number F(i). **Base:** dp[0]=0, dp[1]=1. **Recurrence:** dp[i] = dp[i-1] + dp[i-2].

**Dependency order:** Each cell depends only on the two to its left, so fill left to right.

```
  i:    0   1   2   3   4   5
dp[i]:  0   1   1   2   3   5
        ↑   ↑   ↑
        base  base  dp[2]=dp[1]+dp[0]=1
                         dp[3]=dp[2]+dp[1]=2
                              dp[4]=1+2=3, dp[5]=2+3=5
```

```python
def fib_bottom_up(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**Space optimization:** dp[i] only needs dp[i-1] and dp[i-2], so use two variables and update in a loop (O(1) space).

---

## 18.5 1D DP Classics

### Climbing Stairs

**State:** `dp[i]` = number of ways to reach step i (steps 1 or 2). **Base:** dp[0]=1, dp[1]=1. **Recurrence:** dp[i] = dp[i-1] + dp[i-2].

### House Robber — Worked Example

**Problem:** Rob a row of houses; you cannot rob two adjacent houses. Maximize total money.

**State:** `dp[i]` = maximum money we can get from houses 0..i (we may or may not rob house i).

**Choices at house i:** (1) **Skip** house i → best is dp[i-1]. (2) **Rob** house i → we must skip i-1, so best is nums[i] + dp[i-2].

**Recurrence:** dp[i] = max(dp[i-1], nums[i] + dp[i-2]). Base: dp[0] = nums[0], dp[1] = max(nums[0], nums[1]).

**Example:** nums = [2, 7, 9, 3, 1]

```
  i:      0   1   2   3   4
nums[i]:  2   7   9   3   1
dp[i]:    2   7  11  11  12

  dp[0] = 2
  dp[1] = max(2, 7) = 7
  dp[2] = max(dp[1], 9+dp[0]) = max(7, 11) = 11   (rob 2, skip 1)
  dp[3] = max(11, 3+7) = 11
  dp[4] = max(11, 1+11) = 12   (rob 0,2,4 → 2+9+1=12)
```

Answer: 12.

### Coin Change (Minimum Number of Coins)

**State:** `dp[a]` = minimum number of coins to make amount a. **Recurrence:** dp[a] = 1 + min(dp[a - c] for c in coins if a ≥ c). Base: dp[0] = 0; treat unreachable amounts as infinity.

### Coin Change 2 (Number of Combinations)

**State:** `dp[a]` = number of ways to make amount a. **Recurrence:** For each coin c, dp[a] += dp[a - c]. **Important:** Iterate coins in the outer loop so each combination is counted once (order doesn't create new ways).

---

## 18.6 2D DP Classics

### Longest Common Subsequence (LCS) — Worked Example

**Problem:** Given two strings, find the length of the longest subsequence common to both (subsequence = order preserved, not necessarily contiguous).

**State:** `dp[i][j]` = length of LCS of `text1[0..i-1]` and `text2[0..j-1]`.

**Recurrence:**
- If `text1[i-1] == text2[j-1]`: we can extend the LCS by one → `dp[i][j] = 1 + dp[i-1][j-1]`.
- Else: we skip one character from either string → `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

**Dependency:** Each cell (i, j) depends on (i-1, j-1), (i-1, j), (i, j-1). Fill row by row (or column by column); when computing (i, j), those three are already computed.

**Example:** text1 = "abcde", text2 = "ace". LCS is "ace" → length 3.

```
         ""  a  c  e   (text2)
    ""   0   0  0  0
    a    0   1  1  1
    b    0   1  1  1
    c    0   1  2  2
    d    0   1  2  2
    e    0   1  2  3
 (text1)

  dp[1][1]: 'a'=='a' → 1+dp[0][0]=1
  dp[3][2]: 'c'=='c' → 1+dp[2][1]=1+1=2
  dp[5][3]: 'e'=='e' → 1+dp[4][2]=1+2=3  → answer 3
```

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

### Edit Distance (Levenshtein)

**State:** `dp[i][j]` = minimum number of insert/delete/replace operations to turn word1[:i] into word2[:j]. **Recurrence:** Insert 1+dp[i][j-1]; Delete 1+dp[i-1][j]; Replace (0 if same else 1)+dp[i-1][j-1]. Take the minimum of the three.

### 0/1 Knapsack

**State:** `dp[i][w]` = max value using first i items and weight limit w. **Recurrence:** For each item, either skip → dp[i-1][w], or take (if w ≥ wt[i]) → val[i] + dp[i-1][w - wt[i]]. Can optimize to 1D by iterating w from high to low so we don't overwrite values we still need.

---

## 18.7 DP on Strings, Intervals, Trees

- **Strings:** Often two indices (i, j) for two strings or one string (e.g., longest palindromic substring: dp[i][j] = True if s[i:j+1] is palindrome).
- **Intervals:** Sort by start or end; dp[i] = best using first i intervals; or dp[i][j] for interval i to j.
- **Trees:** Return (best_including_root, best_excluding_root) or similar; combine from left and right subtrees. (See tree DP in Chapter 6 style.)

---

## 18.8 How to Identify DP

1. **Minimum/maximum/count** over choices or sequences.
2. **Try** defining state (e.g., "dp[i] = best for first i elements").
3. **Recurrence:** How does state i depend on earlier states?
4. **Order:** Fill table so dependencies are ready (e.g., left-to-right for 1D).

**Dependency direction (1D):** Typically `dp[i]` depends on `dp[i-1]`, `dp[i-2]`, etc., so we fill from 0 to n:

```
  dp[0] → dp[1] → dp[2] → ... → dp[n]
   ↑        ↑        ↑
  base   depends  depends on
          on [0]   [0],[1]
```

**Dependency direction (2D):** For LCS, `dp[i][j]` depends on `dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]`. Fill row by row, left to right (or column by column), so those three cells are already computed when we reach (i, j).

---

## 18.9 Complexity

**Time:** Usually # states × work per state (e.g., O(n) for 1D, O(n²) for 2D). **Space:** Same or optimized (e.g., 1D for knapsack).

---

## Practice Exercises

**E1.** Climbing Stairs — 1D, dp[i] = dp[i-1] + dp[i-2].

**E2.** House Robber — 1D, take or skip; two variables.

**E3.** Coin Change — 1D, min coins for amount.

**E4.** Longest Increasing Subsequence — 1D dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i]); or patience sort O(n log n).

**E5.** Longest Common Subsequence — 2D.

**E6.** Edit Distance — 2D.

**E7.** 0/1 Knapsack — 2D then 1D.

**E8.** Word Break — dp[i] = can segment s[:i]; for each word, check suffix match.

**E9.** Maximum Product Subarray — track max and min (negative × negative).

---

## Chapter Summary

| Type | Examples |
|------|----------|
| 1D | Fibonacci, stairs, robber, coin change, LIS |
| 2D | LCS, edit distance, knapsack |
| State definition | Index, (index, constraint), (i, j) |
| Top-down vs bottom-up | Memoization vs table |

**Previous:** [Chapter 17 → Recursion & Backtracking](17_recursion_backtracking.md) | **Next:** [Chapter 19 → Greedy](19_greedy.md)
