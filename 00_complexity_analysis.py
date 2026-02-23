"""
================================================================
00 — COMPLEXITY ANALYSIS
================================================================
The foundation of all algorithmic thinking. Before writing any
solution, you must be able to reason about how it scales.

TOPICS:
  1. Big O Notation
  2. Time Complexity
  3. Space Complexity
  4. Amortized Analysis
  5. Common Complexity Classes
  6. Recurrence Relations
================================================================
"""

# ----------------------------------------------------------------
# 1. BIG O NOTATION
# ----------------------------------------------------------------
"""
Big O describes the UPPER BOUND on how an algorithm's resource
usage (time or space) grows relative to input size n.

We care about the DOMINANT TERM and DROP CONSTANTS:
  - O(2n)       → O(n)
  - O(n + n²)   → O(n²)
  - O(n log n + n) → O(n log n)

Common complexities from fastest to slowest:
  O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
"""

# ----------------------------------------------------------------
# 2. TIME COMPLEXITY EXAMPLES
# ----------------------------------------------------------------

def constant_time(arr):
    """O(1) — does not depend on input size."""
    return arr[0] if arr else None

def logarithmic_time(n):
    """O(log n) — input is halved each step (binary search style)."""
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count

def linear_time(arr):
    """O(n) — one pass through the data."""
    total = 0
    for x in arr:
        total += x
    return total

def linearithmic_time(arr):
    """O(n log n) — e.g. merge sort, heap sort, most efficient comparison sorts."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = linearithmic_time(arr[:mid])
    right = linearithmic_time(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quadratic_time(arr):
    """O(n²) — nested loops over the input."""
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1  # e.g., comparing all pairs
    return count

def exponential_time(n):
    """O(2ⁿ) — e.g., generating all subsets, naive Fibonacci."""
    if n <= 1:
        return n
    return exponential_time(n - 1) + exponential_time(n - 2)  # naive fib

def factorial_time(n):
    """O(n!) — e.g., generating all permutations."""
    if n <= 1:
        return [[]]
    result = []
    sub = factorial_time(n - 1)
    for perm in sub:
        for i in range(len(perm) + 1):
            result.append(perm[:i] + [n] + perm[i:])
    return result

# ----------------------------------------------------------------
# 3. SPACE COMPLEXITY
# ----------------------------------------------------------------
"""
Space complexity counts EXTRA memory used (excluding input).

Types of space:
  - Stack space  — recursion call frames
  - Heap space   — dynamic allocations (lists, dicts, etc.)
  - Auxiliary    — temporary variables

Note: Input space is usually excluded from the analysis unless
the problem requires in-place modification.
"""

def space_O1(arr):
    """O(1) extra space — only a few variables."""
    total = 0
    for x in arr:
        total += x
    return total

def space_On(arr):
    """O(n) extra space — creates a copy or auxiliary structure."""
    seen = set()
    for x in arr:
        seen.add(x)
    return seen

def space_recursion(n):
    """O(n) stack space — one frame per recursive call."""
    if n == 0:
        return 0
    return n + space_recursion(n - 1)

# ----------------------------------------------------------------
# 4. AMORTIZED ANALYSIS
# ----------------------------------------------------------------
"""
Amortized analysis looks at the AVERAGE cost per operation over
a sequence of operations, even if some individual operations are costly.

Classic example: Dynamic Array (Python list)
  - Appending usually O(1)
  - Occasionally O(n) when resizing (doubling strategy)
  - Amortized cost per append: O(1)

Think of it as "paying ahead" for expensive operations.
"""

class DynamicArray:
    """Illustrates amortized O(1) append."""
    def __init__(self):
        self._data = [None]
        self._size = 0
        self._capacity = 1

    def append(self, val):
        if self._size == self._capacity:
            self._resize()                 # O(n) but happens rarely
        self._data[self._size] = val
        self._size += 1

    def _resize(self):
        new_cap = self._capacity * 2       # double capacity
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_cap

    def __len__(self):
        return self._size

# ----------------------------------------------------------------
# 5. COMPLEXITY OF COMMON OPERATIONS
# ----------------------------------------------------------------
"""
Python Built-in Complexities (important to know):

LIST:
  append(x)          O(1) amortized
  pop()              O(1)
  pop(i)             O(n)
  insert(i, x)       O(n)
  del arr[i]         O(n)
  arr[i]             O(1)
  len(arr)           O(1)
  x in arr           O(n)
  arr.sort()         O(n log n)
  arr[:k]            O(k)

DICT (hash map):
  d[key]             O(1) average
  d[key] = val       O(1) average
  key in d           O(1) average
  del d[key]         O(1) average

SET:
  s.add(x)           O(1) average
  x in s             O(1) average
  s.remove(x)        O(1) average

HEAPQ:
  heapq.heappush     O(log n)
  heapq.heappop      O(log n)
  heapq.heapify      O(n)

STRING:
  s + t              O(len(s) + len(t))  — creates new string
  s[i]               O(1)
  s[i:j]             O(j - i)
  len(s)             O(1)
"""

# ----------------------------------------------------------------
# 6. RECURRENCE RELATIONS
# ----------------------------------------------------------------
"""
Recurrences describe recursive algorithms. Solve with Master Theorem:
  T(n) = aT(n/b) + f(n)

  where a = # subproblems, b = size reduction factor, f(n) = work at each level.

Case 1: f(n) = O(n^c) where c < log_b(a)  →  T(n) = O(n^log_b(a))
Case 2: f(n) = O(n^c) where c = log_b(a)  →  T(n) = O(n^c * log n)
Case 3: f(n) = O(n^c) where c > log_b(a)  →  T(n) = O(f(n))

Common examples:
  Binary Search:   T(n) = T(n/2) + O(1)          → O(log n)
  Merge Sort:      T(n) = 2T(n/2) + O(n)         → O(n log n)
  Quick Sort avg:  T(n) = 2T(n/2) + O(n)         → O(n log n)
  Quick Sort worst: T(n) = T(n-1) + O(n)         → O(n²)
  Binary Tree DFS: T(n) = 2T(n/2) + O(1)         → O(n)
"""

# ----------------------------------------------------------------
# PRACTICE QUESTIONS
# ----------------------------------------------------------------
"""
Q1 (Easy): What is the time complexity of this function?
    def foo(n):
        for i in range(n):
            for j in range(10):
                print(i, j)
Answer: O(n) — inner loop is constant (10 iterations).

Q2 (Easy): What is the time and space complexity of reversing a string
    s = s[::-1]
Answer: Time O(n), Space O(n) — creates a new string.

Q3 (Medium): Analyze the complexity of this function:
    def bar(arr):
        result = []
        for i in range(len(arr)):
            result.append(arr[i])
            result.sort()
        return result
Answer: Time O(n² log n), Space O(n)
    — sort inside loop: O(n log n) * n iterations.

Q4 (Medium): What is the space complexity of a recursive DFS on a tree with n nodes?
Answer: O(h) where h is height. Worst case O(n) for skewed tree, O(log n) for balanced.

Q5 (Hard): You have two nested loops:
    for i in range(n):
        j = i
        while j < n:
            j *= 2
    What is the total time complexity?
Answer: O(n log n) — outer is O(n), inner does O(log n) work for each i.

Q6 (Hard): Prove that the amortized cost of append to a dynamic array is O(1).
Hint: Use the potential method. Total cost = actual cost + change in potential.
    Set Φ = 2*size - capacity.
    On cheap insert: actual = 1, ΔΦ = 2, amortized = 3 = O(1)
    On resize (n inserts): actual = n + n (copy), ΔΦ = -(n), amortized = n+n-n = n → O(1) each.
"""

if __name__ == "__main__":
    # Demonstrate growth rates
    import time

    sizes = [100, 1000, 10000]
    print("n\t\tlog n\t\tn\t\tn log n\t\tn²")
    for n in sizes:
        import math
        print(f"{n}\t\t{math.log2(n):.1f}\t\t{n}\t\t{n * math.log2(n):.0f}\t\t{n**2}")
