# Chapter 14: Binary Search

> *"Binary search isn't just 'find in sorted array.' It's 'find the boundary where the condition flips.'"*

---

## 14.1 Why Binary Search Matters

Binary search gives **O(log n)** when the space is **sorted** or **monotonic** (condition true for first half, false for second, or vice versa). Classic use: find index in sorted array. Same idea extends to **search space**: "smallest x such that f(x) is true" (lower bound) or "largest x such that f(x) is true" (upper bound). Interview favorites: rotated sorted array, search 2D matrix, "binary search on the answer" (e.g., capacity, threshold). One off-by-one mistake can break it — use a **consistent template**.

---

## 14.2 Classic Template (Find Target in Sorted Array)

**Closed range [left, right];** exit when `left > right`. Mid = (left + right) // 2. Compare with target and **discard one half**; reduce range by one each time to avoid infinite loop.

### Worked Example: Find 7 in Sorted Array

```
arr = [1, 3, 5, 7, 9, 11],  target = 7
       left        mid        right

Step 1: left=0, right=5 → mid=2; arr[2]=5 < 7 → discard left half, left=3
Step 2: left=3, right=5 → mid=4; arr[4]=9 > 7 → discard right half, right=3
Step 3: left=3, right=3 → mid=3; arr[3]=7 == 7 → return 3
```

Each step halves the search space; for n elements we need at most ⌈log₂ n⌉ steps.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Avoid overflow in other languages:** `mid = left + (right - left) // 2`.

---

## 14.3 Lower Bound and Upper Bound

- **Lower bound:** Smallest index i such that arr[i] >= target (first position where we can insert target and keep sorted). If all elements < target, return len(arr).
- **Upper bound:** Smallest index i such that arr[i] > target. So "last position of target" = upper_bound - 1.

**Example:** arr = [1, 2, 2, 2, 3], target = 2.
- lower_bound(2) = 1 (first index where arr[i] >= 2).
- upper_bound(2) = 4 (first index where arr[i] > 2).
- Range of 2: indices [1, 3]. Count = 4 - 1 = 3.

```python
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

def upper_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left
```

**Range of target:** [lower_bound(target), upper_bound(target) - 1]. Count of target = upper_bound - lower_bound.

---

## 14.4 Rotated Sorted Array

Array was sorted then rotated (e.g., [4,5,6,7,0,1,2]). **Find target:** Compare mid with left (or right) to know which half is sorted; then check if target is in that half.

```python
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

**Find minimum in rotated array:** Same idea — go toward the unsorted half (the one that contains the pivot). Compare mid with right: if arr[mid] < arr[right], min is in left half (including mid); else in right half.

---

## 14.5 Search in 2D Matrix (Sorted by Rows and Columns)

Matrix: each row sorted left to right; each column sorted top to bottom. **Start from top-right** (or bottom-left): if current > target, move left; if current < target, move down. O(m + n).  
If matrix is "sorted in row-major order" (first row, then second row, ...), flatten to 1D indices: row = mid // cols, col = mid % cols; run normal binary search.

---

## 14.6 Binary Search on the Answer

**Idea:** The answer is in a range [low, high]. For a candidate value `mid`, check if it's "feasible." If feasible, try smaller (or larger); else try larger (or smaller). Example: "minimum capacity to ship in D days" — feasible(cap) = can ship with capacity cap in ≤ D days; binary search on cap.

```python
def min_capacity(weights, days):
    def feasible(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = w
            else:
                cur += w
            if d > days:
                return False
        return True

    low, high = max(weights), sum(weights)
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid + 1
    return low
```

---

## 14.7 Common Pitfalls

- **Infinite loop:** Use `left <= right` with `mid±1`, or `left < right` with `right = mid` (no +1 on the branch that keeps mid). Don't leave both ends unchanged.
- **Wrong bound:** Decide whether you want first occurrence (lower_bound) or last (upper_bound - 1).
- **Range:** Use [0, n] for lower/upper bound so "not found" returns n; use [0, n-1] for classic find.

---

## 14.8 Complexity

**Time:** O(log n) per search. **Space:** O(1).

---

## Practice Exercises

**E1.** Binary Search — classic template.

**E2.** Search Insert Position — lower_bound.

**E3.** Find First and Last Position — lower_bound and upper_bound.

**E4.** Search in Rotated Sorted Array — which half is sorted, then narrow.

**E5.** Koko Eating Bananas / Minimum capacity — binary search on answer; feasible(mid).

**E6.** Search a 2D Matrix (row-major sorted) — flatten index.

**E7.** Median of Two Sorted Arrays — binary search on the smaller array's partition; check cross elements for correct split.

---

## Chapter Summary

| Pattern | Use |
|---------|-----|
| Classic | Sorted array, exact match |
| Lower/upper bound | First/last position, count |
| Rotated array | Compare mid with left/right, go to sorted half |
| 2D matrix | Top-right walk or flatten |
| Binary search on answer | Feasible(mid), shrink range |

**Previous:** [Chapter 13 → Sorting](13_sorting.md) | **Next:** [Chapter 15 → Two Pointers](15_two_pointers.md)
