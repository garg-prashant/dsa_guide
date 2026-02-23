# Chapter 20: Divide & Conquer

> *"Split the problem, solve the parts, combine the answers. Recurrence analysis tells you the cost."*

---

## 20.1 Why Divide & Conquer Matters

**Divide & Conquer** splits a problem into **smaller subproblems** of the same type, solves them (usually recursively), and **combines** the results. Merge sort and quick sort are classic examples; binary search is D&C that only recurses into one half. **Master theorem** gives the asymptotic cost of recurrences T(n) = a·T(n/b) + f(n). Interviews may ask "design an O(n log n) algorithm" or "analyze this recurrence" — D&C is the standard approach.

---

## 20.2 Paradigm

1. **Divide:** Split into smaller instances (e.g., left half, right half).
2. **Conquer:** Solve subproblems (base case when small enough).
3. **Combine:** Merge results (e.g., merge two sorted halves).

---

## 20.3 Master Theorem

For T(n) = a·T(n/b) + Θ(n^k) where a ≥ 1, b > 1:

- If log_b(a) > k: T(n) = Θ(n^(log_b(a))).
- If log_b(a) = k: T(n) = Θ(n^k log n).
- If log_b(a) < k: T(n) = Θ(n^k).

Example: Merge sort T(n) = 2T(n/2) + Θ(n) → a=2, b=2, k=1 → log_2(2)=1=k → Θ(n log n).

---

## 20.4 Merge Sort and Quick Sort (Revisited)

**Merge sort:** Divide into two halves; conquer (sort each); combine (merge in Θ(n)). T(n) = 2T(n/2) + Θ(n) = Θ(n log n). See **Chapter 13**.

**Quick sort:** Pick pivot; partition; conquer left and right. T(n) = T(k) + T(n-k-1) + Θ(n). Average k ≈ n/2 → Θ(n log n); worst k=0 → Θ(n²). See **Chapter 13**.

---

## 20.5 Quick Select (K-th Smallest)

Partition like quick sort; recurse only on the half that contains the k-th element. Average Θ(n); worst Θ(n²). Can be made expected Θ(n) with random pivot.

```python
def quick_select(arr, k):
    # 0-indexed k; returns k-th smallest element
    def partition(l, r):
        pivot = arr[r]
        i = l
        for j in range(l, r):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[r] = arr[r], arr[i]
        return i
    left, right = 0, len(arr) - 1
    while True:
        p = partition(left, right)
        if p == k:
            return arr[p]
        if p < k:
            left = p + 1
        else:
            right = p - 1
```

---

## 20.6 Binary Search as D&C

Split by comparing with mid; recurse on one half. T(n) = T(n/2) + Θ(1) = Θ(log n). See **Chapter 14**.

---

## 20.7 Other Examples

**Closest pair of points:** Split by x; find closest in left and right; combine by checking points near the midline (within strip of width 2d where d = min(left_ans, right_ans)). Θ(n log n).

**Strassen's matrix multiplication (conceptual):** Multiply 2×2 blocks with 7 multiplications instead of 8; recurse. Θ(n^log2(7)) ≈ Θ(n^2.81).

**Maximum subarray (Kadane is simpler):** D&C: max subarray is either in left half, right half, or crossing mid. Cross-middle: expand from mid left and right. T(n) = 2T(n/2) + Θ(n) = Θ(n log n). (Kadane is Θ(n).)

---

## 20.8 When to Use D&C

- Problem can be split into **similar subproblems** and answers **combined**.
- You want **O(n log n)** or recurrence fits master theorem.
- **Binary search** when the space is monotonic; **merge/quick** when sorting or selecting.

---

## Practice Exercises

**E1.** Sort an array — merge sort or quick sort.

**E2.** Kth Largest Element — quick select or heap (Chapter 7).

**E3.** Different Ways to Add Parentheses — for each operator, divide left and right; combine results with that operator.

**E4.** Maximum Subarray — Kadane (DP) or D&C (crossing mid).

---

## Chapter Summary

| Problem | D&C Approach |
|---------|----------------|
| Sorting | Merge sort, quick sort |
| Selection | Quick select |
| Search | Binary search |
| Recurrence | Master theorem |

**Previous:** [Chapter 19 → Greedy](19_greedy.md) | **Next:** [Chapter 21 → Graph Algorithms](21_graph_algorithms.md)
