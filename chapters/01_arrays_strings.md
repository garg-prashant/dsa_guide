# Chapter 1: Arrays & Strings

> *"Arrays are the backbone of algorithms. Master them and everything else becomes clearer."*

---

## 1.1 What Is an Array?

An **array** is a contiguous block of memory that stores elements of the same type. Each element is accessible in **O(1)** time via its index — because the address of element i is simply `base_address + i × element_size`.

```
Index:   0    1    2    3    4
Value: [ 10 | 20 | 30 | 40 | 50 ]
         ↑
    base address
```

In Python, the built-in `list` is a **dynamic array** — it can grow and shrink, and stores references to objects (so it can hold mixed types).

### Python List Internals
Python's list over-allocates memory to support amortized O(1) appends. When the array fills up, it doubles its capacity.

```python
import sys

arr = []
for i in range(10):
    arr.append(i)
    print(f"len={len(arr)}, sys.getsizeof={sys.getsizeof(arr)} bytes")
# Notice size jumps at 4 → 8 → 16 → ... (doubling strategy)
```

---

## 1.2 Core Operations & Complexity

| Operation | Code | Time | Notes |
|-----------|------|------|-------|
| Access | `arr[i]` | O(1) | Direct index |
| Update | `arr[i] = x` | O(1) | Direct index |
| Append | `arr.append(x)` | O(1)* | Amortized |
| Pop from end | `arr.pop()` | O(1) | |
| Insert at i | `arr.insert(i, x)` | O(n) | Shifts elements right |
| Delete at i | `del arr[i]` | O(n) | Shifts elements left |
| Search | `x in arr` | O(n) | Linear scan |
| Slice | `arr[i:j]` | O(j-i) | Creates new list |
| Length | `len(arr)` | O(1) | Cached |

---

## 1.3 Strings in Python

Strings are **immutable sequences** of characters. This has important consequences:

```python
s = "hello"
# s[0] = 'H'  ← TypeError: strings don't support item assignment

# Every string operation that "modifies" a string creates a NEW one
s2 = s + " world"   # O(n + m) — allocates new memory

# ✅ Build strings efficiently with join
parts = ["a", "b", "c", "d"]
result = "".join(parts)  # O(n) — one allocation
# vs
result = ""
for p in parts:
    result += p   # O(n²) — creates a new string each time!
```

> **Key Insight:** String concatenation in a loop is O(n²). Always use `"".join()` to build strings.

### Useful String Methods
```python
s = "Hello, World!"

s.lower()           # "hello, world!"
s.upper()           # "HELLO, WORLD!"
s.strip()           # removes leading/trailing whitespace
s.split(",")        # ["Hello", " World!"]
s.replace("l", "x") # "Hexxo, Worxd!"
s.startswith("He")  # True
s.endswith("!")     # True
s.find("World")     # 7  (index of first occurrence)
s.count("l")        # 3
s.isdigit()         # False
s.isalpha()         # False
s[::-1]             # "!dlroW ,olleH"  (reverse)
sorted(s)           # list of sorted characters
```

---

## 1.4 Key Techniques

### Technique 1: Prefix Sums

**Problem pattern:** "Find subarray sum equal to k", "Range sum queries"

The prefix sum array `prefix[i]` = sum of `arr[0..i-1]`. Then:
- Sum of `arr[l..r]` = `prefix[r+1] - prefix[l]`

```
arr    =  [ 1,  3, -2,  4,  2]
prefix =  [ 0,  1,  4,  2,  6,  8]
             ↑
           prefix[0] = 0 (sentinel)

Sum of arr[1..3] = prefix[4] - prefix[1] = 6 - 1 = 5
                 = 3 + (-2) + 4 = 5  ✓
```

```python
def build_prefix(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, l, r):
    """Sum of arr[l..r] inclusive."""
    return prefix[r + 1] - prefix[l]

# Example: Subarray Sum Equals K
def subarray_sum(arr, k):
    """Count subarrays with sum equal to k. O(n) time, O(n) space."""
    count = 0
    prefix_sum = 0
    seen = {0: 1}  # prefix_sum → frequency

    for x in arr:
        prefix_sum += x
        # If prefix_sum - k exists, we found a valid subarray
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1

    return count
```

---

### Technique 2: Kadane's Algorithm (Maximum Subarray)

**Problem:** Find the contiguous subarray with the largest sum.

**Key Insight:** At each position, we decide: extend the current subarray, or start fresh here.

```
arr = [-2,  1, -3,  4, -1,  2,  1, -5,  4]

Step by step (current_sum = max to include current element):
  i=0: current=-2, max_sum=-2
  i=1: current=max(1, -2+1)=1,  max_sum=1
  i=2: current=max(-3, 1-3)=-2, max_sum=1
  i=3: current=max(4, -2+4)=4,  max_sum=4
  i=4: current=max(-1, 4-1)=3,  max_sum=4
  i=5: current=max(2, 3+2)=5,   max_sum=5
  i=6: current=max(1, 5+1)=6,   max_sum=6
  i=7: current=max(-5, 6-5)=1,  max_sum=6
  i=8: current=max(4, 1+4)=5,   max_sum=6

Answer: 6  (subarray [4, -1, 2, 1])
```

```python
def max_subarray(arr):
    """Kadane's Algorithm. O(n) time, O(1) space."""
    max_sum = current_sum = arr[0]

    for x in arr[1:]:
        current_sum = max(x, current_sum + x)
        max_sum = max(max_sum, current_sum)

    return max_sum
```

---

### Technique 3: In-Place Reversal

Swap elements from the outside in. No extra space needed.

```
arr = [1, 2, 3, 4, 5]
       ↑              ↑
      lo             hi

Step 1: swap(0, 4) → [5, 2, 3, 4, 1]
Step 2: swap(1, 3) → [5, 4, 3, 2, 1]
Step 3: lo ≥ hi, stop.
```

```python
def reverse_array(arr, lo=0, hi=None):
    """Reverse arr[lo..hi] in place. O(n) time, O(1) space."""
    if hi is None:
        hi = len(arr) - 1
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        lo += 1
        hi -= 1
```

---

### Technique 4: Sorting as a Preprocessing Step

Many array problems become trivial after sorting.

```python
# Two Sum — sorted version with two pointers
def two_sum_sorted(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []

# Three Sum — reduce to two sum
def three_sum(arr):
    arr.sort()
    result = []
    for i in range(len(arr) - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue  # skip duplicates
        lo, hi = i + 1, len(arr) - 1
        while lo < hi:
            s = arr[i] + arr[lo] + arr[hi]
            if s == 0:
                result.append([arr[i], arr[lo], arr[hi]])
                while lo < hi and arr[lo] == arr[lo + 1]:
                    lo += 1
                while lo < hi and arr[hi] == arr[hi - 1]:
                    hi -= 1
                lo += 1; hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return result
```

---

## 1.5 Classic Problems, Fully Solved

### Problem 1: Best Time to Buy and Sell Stock
*Given prices on each day, find max profit from one buy and one sell.*

**Approach:** Track the minimum price seen so far. At each day, compute profit if we sell today.

```python
def max_profit(prices):
    """O(n) time, O(1) space."""
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit

# Test
print(max_profit([7, 1, 5, 3, 6, 4]))  # 5 (buy at 1, sell at 6)
print(max_profit([7, 6, 4, 3, 1]))     # 0 (prices only fall)
```

---

### Problem 2: Product of Array Except Self
*Return array where each element is the product of all other elements. No division.*

**Approach:** For each index i, product = (product of all elements left of i) × (product of all elements right of i).

```
arr = [1, 2, 3, 4]

Left products:   [1, 1, 2, 6]    (prefix products)
Right products:  [24, 12, 4, 1]  (suffix products)
Answer:          [24, 12, 8, 6]
```

```python
def product_except_self(arr):
    """O(n) time, O(1) extra space (output array doesn't count)."""
    n = len(arr)
    result = [1] * n

    # First pass: result[i] = product of everything to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= arr[i]

    # Second pass: multiply by product of everything to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= arr[i]

    return result

print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]
```

---

### Problem 3: Valid Anagram
*Given two strings s and t, return true if t is an anagram of s.*

```python
def is_anagram(s, t):
    """O(n) time, O(1) space (26 letters = constant)."""
    if len(s) != len(t):
        return False

    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    for c in t:
        count[ord(c) - ord('a')] -= 1

    return all(x == 0 for x in count)

# Simpler but same complexity:
from collections import Counter
def is_anagram_v2(s, t):
    return Counter(s) == Counter(t)
```

---

### Problem 4: Rotate Array
*Rotate array to the right by k steps in place.*

**Key Trick:** Rotate = Reverse all + Reverse first k + Reverse rest.

```
arr = [1, 2, 3, 4, 5, 6, 7], k = 3

Reverse all:        [7, 6, 5, 4, 3, 2, 1]
Reverse first 3:    [5, 6, 7, 4, 3, 2, 1]
Reverse rest:       [5, 6, 7, 1, 2, 3, 4]  ✓
```

```python
def rotate(arr, k):
    """O(n) time, O(1) space."""
    n = len(arr)
    k %= n  # handle k > n

    def reverse(lo, hi):
        while lo < hi:
            arr[lo], arr[hi] = arr[hi], arr[lo]
            lo += 1; hi -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

---

## Practice Exercises

### Easy

**E1.** Given an integer array, return `True` if any value appears at least twice.
```
Input: [1, 2, 3, 1]  → True
Input: [1, 2, 3, 4]  → False
```
<details>
<summary>Hint</summary>
Use a set. Add each element; if it's already in the set, return True.
Time: O(n), Space: O(n).
</details>

---

**E2.** Given a string, return the character that appears most often. If tie, return any.
<details>
<summary>Hint</summary>
Use `collections.Counter`. Then `max(counter, key=counter.get)`.
</details>

---

**E3.** Move all zeros to the end of the array in place, maintaining relative order of non-zero elements.
```
Input: [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```
<details>
<summary>Hint</summary>
Use a write pointer. Iterate and copy non-zero elements to write pointer position. Fill rest with zeros.
</details>

---

### Medium

**E4.** Given an integer array and an integer k, return the number of subarrays whose sum equals k.
```
Input: arr=[1, 1, 1], k=2  → 2
```
<details>
<summary>Hint</summary>
Prefix sums + hash map. Key insight: if prefix[j] - prefix[i] = k, then subarray [i+1..j] sums to k.
</details>

---

**E5.** Given an array of integers, find the length of the longest consecutive sequence.
```
Input: [100, 4, 200, 1, 3, 2]  → 4 (sequence: 1, 2, 3, 4)
```
<details>
<summary>Hint</summary>
Put all numbers in a set. For each number n where n-1 is NOT in the set (sequence start), count how long the sequence extends.
Time: O(n), Space: O(n).
</details>

---

**E6.** You are given an integer array and you must return indices of the two numbers that add up to a target. Each input has exactly one solution.
```
Input: [2, 7, 11, 15], target=9  → [0, 1]
```
<details>
<summary>Hint</summary>
Hash map: for each element x, check if target-x is in the map. Store x → index as you go.
</details>

---

### Hard

**E7.** Given an m×n matrix, if an element is 0, set its entire row and column to 0 in place.
<details>
<summary>Hint</summary>
First pass: record which rows/cols have zeros. Second pass: zero them out.
Space-optimized: use first row and first column as markers (be careful with the [0][0] cell).
</details>

---

**E8.** Given an array of n integers, find three integers such that the sum is closest to target.
<details>
<summary>Hint</summary>
Sort the array. For each element arr[i], use two pointers on arr[i+1..n-1]. Track closest sum.
Time: O(n²).
</details>

---

**E9.** Given a string containing just `(`, `)`, `{`, `}`, `[`, `]`, determine if the input string is valid.
<details>
<summary>Hint</summary>
Use a stack. On open bracket, push it. On close bracket, pop and verify it matches.
</details>

---

## Chapter Summary

| Technique | When to Use | Complexity |
|-----------|-------------|-----------|
| Prefix Sums | Range queries, subarray sums | O(n) build, O(1) query |
| Kadane's | Maximum subarray | O(n) time, O(1) space |
| In-Place Reversal | Rotate array | O(n) time, O(1) space |
| Sorting + Two Pointers | Pair/triplet sums | O(n log n) |
| Hash Map | Two Sum, frequency counts | O(n) time, O(n) space |
| `"".join()` | Building strings | O(n) vs O(n²) for concatenation |

**Previous:** [Chapter 0 → Complexity Analysis](00_complexity.md) | **Next:** [Chapter 2 → Linked Lists](02_linked_lists.md)
