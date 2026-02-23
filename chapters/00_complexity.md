# Chapter 0: Complexity Analysis

> *Before writing a single line of code, ask: "How will this scale?"*

---

## 0.1 Why Complexity Matters

Imagine you're searching for a name in a phonebook with a million entries. You could start from page 1 and check every name — that's a **linear** search. Or you could open to the middle, decide which half contains the name, and repeat — that's a **binary** search.

Both find the name. But one takes up to 1,000,000 steps; the other takes at most 20. **That difference is complexity analysis.**

In interviews, a working solution is not enough. You must communicate *why* your solution is efficient — or acknowledge when it isn't, and propose improvements.

---

## 0.2 Big O Notation

**Big O** expresses how an algorithm's resource usage grows as the input size *n* grows. It gives an **upper bound** — the worst-case behavior.

### Formal Definition
> f(n) is O(g(n)) if there exist constants c > 0 and n₀ such that f(n) ≤ c·g(n) for all n ≥ n₀.

In practice, this means: **drop constants, keep the dominant term.**

| Expression | Simplified |
|------------|-----------|
| O(3n) | O(n) |
| O(n² + n) | O(n²) |
| O(2n + 100) | O(n) |
| O(n² + n log n) | O(n²) |
| O(n · n · n) | O(n³) |

---

## 0.3 Common Complexity Classes

Listed from fastest (best) to slowest (worst):

### O(1) — Constant Time
The algorithm always does the same amount of work, regardless of input size.

```python
def get_first(arr):
    return arr[0]  # Always one operation

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]  # Always three operations
```

**Examples:** Array access by index, hash table lookup (average), push/pop on a stack.

---

### O(log n) — Logarithmic Time
The input is divided (usually halved) at each step. Extremely efficient.

```python
def binary_search(arr, target):
    """Each step eliminates half the remaining search space."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1      # Eliminate left half
        else:
            hi = mid - 1      # Eliminate right half
    return -1
```

**Trace through:** n=16 → 8 → 4 → 2 → 1 (4 steps = log₂(16) = 4)

**Examples:** Binary search, tree height of a balanced BST, heap operations.

---

### O(n) — Linear Time
One pass through the data. Proportional to input size.

```python
def find_max(arr):
    """Visit every element exactly once."""
    max_val = arr[0]
    for x in arr:           # n iterations
        if x > max_val:
            max_val = x
    return max_val
```

**Examples:** Linear search, summing an array, checking if a string is a palindrome.

---

### O(n log n) — Linearithmic Time
The sweet spot for sorting algorithms. Efficient but not trivial.

```python
def merge_sort(arr):
    """Divide the array (log n levels), merge at each level (n work)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

**Examples:** Merge sort, heap sort, Tim sort (Python's built-in), many divide & conquer algorithms.

---

### O(n²) — Quadratic Time
Two nested loops over the input. Acceptable only for small n (n ≤ 10³).

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):          # n iterations
        for j in range(n - i - 1):  # ~n iterations
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

**Examples:** Bubble sort, selection sort, naïve string matching.

---

### O(2ⁿ) — Exponential Time
Doubles with each added element. Acceptable only for n ≤ 20.

```python
def fibonacci_naive(n):
    """Recomputes the same subproblems over and over."""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
    # Draws a tree with ~2^n nodes
```

**Examples:** Generating all subsets, naive Fibonacci, brute-force combinatorial problems.

---

### O(n!) — Factorial Time
The worst practical complexity. Only for n ≤ 10–12.

```python
def permutations(arr):
    """Generate all orderings of the array."""
    if len(arr) <= 1:
        return [arr[:]]
    result = []
    for i in range(len(arr)):
        arr[0], arr[i] = arr[i], arr[0]
        for perm in permutations(arr[1:]):
            result.append([arr[0]] + perm)
        arr[0], arr[i] = arr[i], arr[0]
    return result
```

**Examples:** Generating all permutations, traveling salesman (brute force).

---

## 0.4 Growth Rate Visualization

```
n = 16    operations per algorithm:
──────────────────────────────────────────────────────
O(1)         1
O(log n)     4
O(√n)        4
O(n)        16
O(n log n)  64
O(n²)      256
O(2ⁿ)   65,536
O(n!)  20,922,789,888,000
```

> **Key Interview Insight:** When n = 10⁵ (typical constraint), you need O(n log n) or better. When n = 10⁶, you likely need O(n) or O(n log n). When n = 10⁹, you need O(log n) or O(1).

---

## 0.5 Space Complexity

Space complexity measures **extra memory** used (not counting the input itself, unless stated otherwise).

### Stack Space from Recursion

```python
def factorial(n):
    # Each call adds a frame to the call stack
    # Depth of recursion = n → O(n) space
    if n == 0:
        return 1
    return n * factorial(n - 1)

def factorial_iterative(n):
    # O(1) space — no recursion
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

### Auxiliary Data Structures

```python
def has_duplicate(arr):
    # O(n) space — we store up to n elements in the set
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False

def has_duplicate_sort(arr):
    # O(1) extra space (O(log n) for sort's call stack)
    arr.sort()
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            return True
    return False
```

---

## 0.6 Amortized Analysis

Some operations are occasionally expensive but cheap on average. **Amortized analysis** captures the average cost per operation over a sequence.

### The Classic Example: Dynamic Array

Python's `list` automatically resizes when full. When it doubles:
- Most appends: **O(1)**
- Occasional resize: **O(n)** — copies all elements

But over *n* appends total, we do at most 2n copy operations (geometric series: n/2 + n/4 + ... ≤ n). So the **amortized cost per append is O(1)**.

```python
class DynamicArray:
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None]

    def append(self, val):
        if self._size == self._capacity:
            # O(n) resize, but happens infrequently
            new_cap = self._capacity * 2
            new_data = [None] * new_cap
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_cap
            self._capacity = new_cap
        self._data[self._size] = val
        self._size += 1
    # Amortized: O(1) per append
```

---

## 0.7 Python Built-in Complexities (Must Know)

```
LIST operations:
  arr[i]              O(1)       — index access
  arr.append(x)       O(1)*      — amortized
  arr.pop()           O(1)       — from end
  arr.pop(i)          O(n)       — shifts elements
  arr.insert(i, x)    O(n)       — shifts elements
  x in arr            O(n)       — linear scan
  arr.sort()          O(n log n) — Timsort

DICT operations:
  d[key]              O(1)*      — average case
  d[key] = val        O(1)*      — average case
  key in d            O(1)*      — average case
  del d[key]          O(1)*      — average case

SET operations:
  s.add(x)            O(1)*      — average case
  x in s              O(1)*      — average case
  s.remove(x)         O(1)*      — average case
  s1 & s2             O(min(|s1|, |s2|))
  s1 | s2             O(|s1| + |s2|)

STRING operations:
  s[i]                O(1)
  s + t               O(n + m)   — creates new string
  s[i:j]              O(j - i)   — slicing
  ''.join(arr)        O(n)       — preferred for building strings

HEAPQ operations:
  heappush(h, x)      O(log n)
  heappop(h)          O(log n)
  heapify(arr)        O(n)       ← linear! Not O(n log n)
  nlargest(k, arr)    O(n log k)
  nsmallest(k, arr)   O(n log k)

* Average case. Hash collisions can degrade to O(n) in worst case.
```

---

## 0.8 Recurrence Relations

Recursive algorithms are analyzed via recurrences. The **Master Theorem** solves many:

> **T(n) = a·T(n/b) + f(n)**
> - a = number of subproblems
> - b = factor by which input shrinks
> - f(n) = work done outside recursion

| Recurrence | Algorithm | Result |
|------------|-----------|--------|
| T(n) = T(n/2) + O(1) | Binary Search | O(log n) |
| T(n) = 2T(n/2) + O(n) | Merge Sort | O(n log n) |
| T(n) = T(n-1) + O(1) | Factorial | O(n) |
| T(n) = T(n-1) + O(n) | Selection Sort | O(n²) |
| T(n) = 2T(n-1) + O(1) | Naïve Fibonacci | O(2ⁿ) |

---

## Practice Exercises

### Easy

**E1.** What is the time complexity of the following function?
```python
def foo(n):
    result = 0
    for i in range(n):
        for j in range(10):   # constant inner loop
            result += 1
    return result
```
<details>
<summary>Answer</summary>

**O(n)** — the inner loop runs exactly 10 times regardless of n, so the total work is 10n = O(n).
</details>

---

**E2.** What is the space complexity of reversing a string `s[::-1]`?
<details>
<summary>Answer</summary>

**O(n)** — Python strings are immutable; slicing creates a new string of length n.
</details>

---

### Medium

**E3.** Analyze time and space complexity:
```python
def bar(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[i])
        result.sort()          # sort grows with each iteration
    return result
```
<details>
<summary>Answer</summary>

**Time: O(n² log n)** — On iteration i, result has i+1 elements and sorting costs O(i log i). Summing from 1 to n: Σ i·log(i) ≈ O(n² log n).

**Space: O(n)** — result grows to size n.
</details>

---

**E4.** A recursive function calls itself twice with input n/2 each time. Work outside recursion is O(n). What is the time complexity?
<details>
<summary>Answer</summary>

**O(n log n)** — T(n) = 2T(n/2) + O(n). By the Master Theorem, this is Case 2: a=2, b=2, f(n)=n, log_b(a) = 1 = degree of f(n). Result: O(n log n).
</details>

---

### Hard

**E5.** What is the time complexity of this function?
```python
def baz(n):
    for i in range(n):          # O(n) outer
        j = i
        while j < n:
            j *= 2              # j doubles each time
```
<details>
<summary>Answer</summary>

**O(n log n)** — For each i, the inner loop runs log(n/i) times (since j starts at i and doubles until n). Summing: Σ_{i=1}^{n} log(n/i) = n·log(n) - log(n!) ≈ O(n log n) by Stirling's approximation.
</details>

---

**E6.** You have a hash table with open addressing (linear probing) that is 90% full. What happens to lookup time? Why might Python's dict never fill beyond ~67%?
<details>
<summary>Answer</summary>

At 90% load factor, the expected number of probes for an unsuccessful lookup in linear probing is O(1/(1-α)²) where α=0.9 → about 50 probes on average. Python's dict resizes at 2/3 capacity (~67%) to maintain O(1) average-case performance by keeping the load factor low.
</details>

---

## Chapter Summary

| Concept | Key Takeaway |
|---------|-------------|
| Big O | Upper bound, drop constants, keep dominant term |
| O(1) | Array index, hash lookup — ideal |
| O(log n) | Binary search, balanced BST — excellent |
| O(n) | Single scan — good |
| O(n log n) | Merge sort — acceptable for sorting |
| O(n²) | Nested loops — avoid for large n |
| Space | Count recursion depth + auxiliary structures |
| Amortized | Average cost over sequence of operations |

**Next:** [Chapter 1 → Arrays & Strings](01_arrays_strings.md)
