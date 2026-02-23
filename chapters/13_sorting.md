# Chapter 13: Sorting Algorithms

> *"Sorting is the gateway to binary search and many optimizations. Know the trade-offs, then use the library."*

---

## 13.1 Why Sorting Matters

Sorting turns unordered data into ordered data so you can **binary search**, use **two pointers**, or apply **greedy** strategies. In interviews you rarely implement sorts from scratch, but you must know **time/space**, **stability**, and **when each is used**. Python's `sort()` and `sorted()` use **Timsort** (merge + insertion), O(n log n) average, stable. This chapter gives you the mental model and code for comparison-based and linear sorts so you can reason about problems and handle "implement quicksort" or "why is this O(n log n)?".

**Stability** means: if two elements compare equal, they keep their original relative order after sorting. This matters when you sort by one key (e.g. name) and then by another (e.g. score) — a stable sort preserves the first ordering when the second key is equal.

---

## 13.2 Comparison-Based Sorts (Overview)

| Algorithm | Time (avg) | Time (worst) | Space | Stable |
|-----------|------------|--------------|-------|--------|
| Bubble | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(1) | No |
| Insertion | O(n²) | O(n²) | O(1) | Yes |
| Merge | O(n log n) | O(n log n) | O(n) | Yes |
| Quick | O(n log n) | O(n²) | O(log n) | No |
| Heap | O(n log n) | O(n log n) | O(1) | No |

**Stable:** Equal elements keep their relative order. **In-place:** O(1) extra space (excluding recursion stack).

---

## 13.3 Bubble Sort

Repeatedly swap adjacent pairs if out of order; the **largest** unsorted element "bubbles" to the end each pass. Stop when a pass has no swaps (array is sorted).

**Idea:** Compare `arr[j]` with `arr[j+1]`; if out of order, swap. After one full pass, the maximum is at the end. Repeat for the remaining prefix.

### Worked Example: Bubble Sort

```
Initial:  [ 5, 2, 8, 1, 9 ]
            ↑  ↑
Pass 1 (j=0..3): swap 5↔2, then 5↔1, ... largest moves right
  j=0: [ 2, 5, 8, 1, 9 ]   (2,5 ok)
  j=1: [ 2, 5, 8, 1, 9 ]   (5,8 ok)
  j=2: [ 2, 5, 1, 8, 9 ]   (8,1 swapped)
  j=3: [ 2, 5, 1, 8, 9 ]   (8,9 ok)
  → 9 is now at end

Pass 2: [ 2, 1, 5, 8, 9 ]  → 8 in place
Pass 3: [ 1, 2, 5, 8, 9 ]  → 5 in place, then 2, 1
Pass 4: no swaps → done.

Result: [ 1, 2, 5, 8, 9 ]
```

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
```

**Why "bubble"?** Large values rise (move right) like bubbles in water.

---

## 13.4 Selection Sort

For each position **i**, find the **minimum** in `arr[i..n-1]` and **swap** it with `arr[i]`. The prefix `arr[0..i-1]` is always sorted; we just extend it by one correct element each time.

### Worked Example: Selection Sort

```
Initial:  [ 5, 2, 8, 1, 9 ]
           i=0: min in [5,2,8,1,9] is 1 at index 3 → swap arr[0]↔arr[3]
           [ 1, 2, 8, 5, 9 ]
           i=1: min in [2,8,5,9] is 2 at index 1 → no swap
           [ 1, 2, 8, 5, 9 ]
           i=2: min in [8,5,9] is 5 at index 3 → swap arr[2]↔arr[3]
           [ 1, 2, 5, 8, 9 ]
           i=3: min in [8,9] is 8 → no swap
           Done: [ 1, 2, 5, 8, 9 ]
```

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        mn = i
        for j in range(i + 1, n):
            if arr[j] < arr[mn]:
                mn = j
        arr[i], arr[mn] = arr[mn], arr[i]
```

**Note:** Selection sort is **not stable**. Example: sorting `[(2,a), (2,b)]` by number can swap and give `[(2,b), (2,a)]`.

---

## 13.5 Insertion Sort

**Build a sorted prefix.** Start with prefix = first element. For each new element, **insert** it into the correct position in the prefix by shifting larger elements one step right.

### Worked Example: Insertion Sort

```
Initial:  [ 5, 2, 8, 1, 9 ]
           Prefix is [5]. Insert 2: shift nothing, 2 < 5 so put 2 before 5.
           [ 2, 5, 8, 1, 9 ]
           Insert 8: 8 > 5, place after 5.
           [ 2, 5, 8, 1, 9 ]
           Insert 1: 1 is smallest, shift 2,5,8 right; put 1 at start.
           [ 1, 2, 5, 8, 9 ]
           Insert 9: at end.
           [ 1, 2, 5, 8, 9 ]
```

Diagram (inserting 1 into `[2, 5, 8, _, _]`):

```
key = 1.  j starts at 2 (index of 8).
  [ 2, 5, 8, 1, 9 ]   arr[j+1] = arr[j] → [ 2, 5, 8, 8, 9 ]; j=1
  [ 2, 5, 8, 8, 9 ]   arr[j+1] = arr[j] → [ 2, 5, 5, 8, 9 ]; j=0
  [ 2, 5, 5, 8, 9 ]   arr[j+1] = arr[j] → [ 2, 2, 5, 8, 9 ]; j=-1, stop
  arr[0] = key → [ 1, 2, 5, 8, 9 ]
```

```python
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

Good for **small or nearly sorted** arrays. Used inside Timsort for runs.

---

## 13.6 Merge Sort (Divide & Conquer)

**Divide:** Split the array in half. **Conquer:** Sort each half (recursively with merge sort). **Combine:** Merge the two sorted halves into one sorted array. Stable, O(n) extra space for the merge step.

### Diagram: Divide and Merge

```
arr = [38, 27, 43, 3, 9, 82, 10]

DIVIDE (split until size 1):
                    [38, 27, 43, 3, 9, 82, 10]
                    /                          \
         [38, 27, 43, 3]                 [9, 82, 10]
         /            \                   /        \
    [38, 27]      [43, 3]            [9, 82]     [10]
    /      \      /     \            /     \        |
  [38]    [27]  [43]   [3]         [9]   [82]    [10]

MERGE (combine sorted halves; arrows show comparisons):
  [38] [27] → [27, 38]     [43] [3] → [3, 43]     [9][82]→[9,82]  [10] stays
  [27, 38] + [3, 43] → [3, 27, 38, 43]           [9, 82] + [10] → [9, 10, 82]
  [3, 27, 38, 43] + [9, 10, 82] → [3, 9, 10, 27, 38, 43, 82]
```

**Merge step (example):** Combine `L = [3, 27, 38]` and `R = [9, 10, 82]`. Compare fronts: 3 vs 9 → take 3; 27 vs 9 → take 9; 27 vs 10 → take 10; 27 vs 82 → take 27; 38 vs 82 → take 38; then append rest of R → `[3, 9, 10, 27, 38, 82]`.

```python
def merge_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    mid = (left + right) // 2
    merge_sort(arr, left, mid)
    merge_sort(arr, mid + 1, right)
    # merge arr[left..mid] and arr[mid+1..right]
    tmp = []
    i, j = left, mid + 1
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            tmp.append(arr[i])
            i += 1
        else:
            tmp.append(arr[j])
            j += 1
    tmp.extend(arr[i:mid+1])
    tmp.extend(arr[j:right+1])
    arr[left:right+1] = tmp
```

---

## 13.7 Quick Sort (Divide & Conquer)

Choose a **pivot** (e.g., last element). **Partition:** Rearrange so every element ≤ pivot is to its left, every element > pivot is to its right. Pivot is now in its final position. **Recurse** on the left and right parts.

### Diagram: Partition Step

```
arr = [7, 2, 1, 6, 8, 5, 3, 4]   pivot = 4 (last)
      low                    high

Partition: move all ≤ 4 to the left using index i (insert position).
  j=0: 7 > 4, do nothing
  j=1: 2 ≤ 4, swap with i=0 → [2, 7, 1, 6, 8, 5, 3, 4], i=1
  j=2: 1 ≤ 4, swap with i=1 → [2, 1, 7, 6, 8, 5, 3, 4], i=2
  j=3: 6 > 4, skip
  j=4: 8 > 4, skip
  j=5: 5 > 4, skip
  j=6: 3 ≤ 4, swap with i=2 → [2, 1, 3, 6, 8, 5, 7, 4], i=3
  Finally: swap pivot (index 7) with i (3) → [2, 1, 3, 4, 8, 5, 7, 6]
                                                      ↑
                                            pivot 4 is in place
  Recurse on [2,1,3] and [8,5,7,6].
```

**Invariant during partition:** `arr[low..i-1]` ≤ pivot, `arr[i..j-1]` > pivot, `arr[j..high-1]` unprocessed, `arr[high]` = pivot.

```python
def partition(arr, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
```

**Pivot choice:** Last (simple), random (reduces worst-case chance), median-of-three. **Worst case:** O(n²) when pivot is always min or max (e.g. already sorted array with last-element pivot).

---

## 13.8 Heap Sort

Build max-heap from array (see **Chapter 7**); repeatedly extract max and place at end. O(n log n), in-place, not stable.

---

## 13.9 Non-Comparison Sorts (Linear When Range Small)

### Counting Sort

When keys are integers in a **small range** [0, k]: count how many times each value appears, then write that many copies in order. **Time** O(n + k), **space** O(k). Stable if you build the output from the end (see exercises).

**Example:** Sort `[4, 1, 3, 4, 3]` with max_val = 4.

```
Count:  value 0 → 0, 1 → 1, 2 → 0, 3 → 2, 4 → 2
Output: [1, 3, 3, 4, 4]
```

```python
def counting_sort(arr, max_val):
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    out = []
    for v in range(max_val + 1):
        out.extend([v] * count[v])
    return out
```

### Radix Sort

Sort by **digits** (least significant first) or characters. Use a **stable** sort (e.g. counting) per digit/character. **Time** O(n · d) where d = number of digits. Good for fixed-length integers or strings (e.g. dates, lexicographic order).

---

## 13.10 Python's sort() and sorted()

- **sorted(iterable)** returns a new list; **list.sort()** sorts in place. Both use **Timsort**.
- **Key:** `sorted(arr, key=lambda x: (x[1], -x[0]))` — sort by second element, then by first descending.
- **Stable:** Yes. So you can sort by secondary key, then primary key.

---

## 13.11 When to Use Which

| Situation | Choice | Reason |
|-----------|--------|--------|
| **General** | `sorted()` / `.sort()` | Timsort: O(n log n), stable, tuned in practice |
| **Stable + guaranteed O(n log n)** | Merge sort | No bad worst case; use when stability matters |
| **In-place, don't care about stability** | Quick sort or heap sort | Quick sort has O(n²) worst case; heap sort is O(n log n) always |
| **Integers in small range [0, k]** | Counting sort | O(n + k) — linear when k = O(n) |
| **Fixed-length integers or strings** | Radix sort | O(n · d) with d = digit length |
| **Nearly sorted or very small n** | Insertion sort | Simple, fast in practice for small inputs |

**Decision flow:** Need linear time and small integer range? → Counting/radix. Need stability? → Merge (or Timsort). Need in-place? → Quick or heap. Otherwise → use the library.

---

## 13.12 Complexity Summary

| Algorithm | Best | Avg | Worst | Space |
|-----------|------|-----|-------|-------|
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) |

---

## Practice Exercises

**E1.** Sort Colors (Dutch national flag) — one pass: three pointers; 0s to left, 2s to right.

**E2.** Merge Intervals — sort by start; merge overlapping.

**E3.** Largest Number — sort strings by custom compare: a+b vs b+a.

**E4.** K Closest Points to Origin — sort by distance² or quickselect/heap.

---

## Chapter Summary

| Need | Choice |
|------|--------|
| General | Timsort / sorted() |
| Stable, guaranteed O(n log n) | Merge sort |
| In-place | Quick sort / heap sort |
| Small integer range | Counting / radix |

**Previous:** [Chapter 12 → Fenwick Trees](12_fenwick_trees.md) | **Next:** [Chapter 14 → Binary Search](14_binary_search.md)
