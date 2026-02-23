# Chapter 15: Two Pointers

> *"Two pointers turn O(n²) into O(n) when the array is sorted or when you can move one pointer based on the other."*

---

## 15.1 Why Two Pointers Matter

**Two pointers** use two indices (or one pointer per sequence) that move in a coordinated way to scan the array (or two arrays) in **O(n)**. Patterns: **opposite ends** (converge from left and right), **same direction** (both move forward, possibly at different speeds), and **fast & slow** (cycle detection). Combined with sorting, you get two-sum, three-sum, and many string/array problems. See also **Chapter 1** (arrays) and **Chapter 16** (sliding window) for overlap.

---

## 15.2 Opposite Ends (Converging)

**Sorted array:** left at start, right at end. If sum too small, left++; if too large, right--. **Two Sum II:** find two numbers that add to target.

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1
        else:
            right -= 1
    return []
```

**Trapping Rain Water:** For each position, water level = min(max_left, max_right) - height[i]. Two pointers: left and right; move the side with smaller max (that side's water level is determined). Or use two passes to precompute max_left/max_right.

```python
def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    max_left, max_right = height[0], height[-1]
    water = 0
    while left < right:
        if max_left <= max_right:
            water += max_left - height[left]
            left += 1
            max_left = max(max_left, height[left])
        else:
            water += max_right - height[right]
            right -= 1
            max_right = max(max_right, height[right])
    return water
```

---

## 15.3 Same Direction (Chase / Window)

Both pointers move forward. **Remove duplicates in place:** reader scans, writer writes only when value changes.

```python
def remove_duplicates(arr):
    if not arr:
        return 0
    w = 1
    for r in range(1, len(arr)):
        if arr[r] != arr[r - 1]:
            arr[w] = arr[r]
            w += 1
    return w
```

**Move zeros to end:** writer = next position for non-zero; reader scans; swap or copy.

---

## 15.4 Fast and Slow (Floyd's Cycle Detection)

**Linked list cycle:** Slow moves 1 step, fast moves 2 steps. If they meet, there's a cycle. **Cycle start:** After meeting, put slow at head; move both 1 step until they meet — that's the cycle start. See **Chapter 2** (linked lists).

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Middle of list:** Fast moves 2, slow moves 1; when fast reaches end, slow is at middle.

---

## 15.5 Three Sum / Four Sum

**Three Sum:** Sort; for each index i, run two pointers on arr[i+1:] for two numbers that sum to -arr[i]. Skip duplicates by advancing pointers past equal values.

```python
def three_sum(arr):
    arr.sort()
    n = len(arr)
    out = []
    for i in range(n):
        if i and arr[i] == arr[i-1]:
            continue
        left, right = i + 1, n - 1
        target = -arr[i]
        while left < right:
            s = arr[left] + arr[right]
            if s == target:
                out.append([arr[i], arr[left], arr[right]])
                left += 1
                while left < right and arr[left] == arr[left-1]:
                    left += 1
                right -= 1
                while left < right and arr[right] == arr[right+1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return out
```

**Four Sum:** Fix two indices i, j; two pointers on the rest for two numbers summing to target - arr[i] - arr[j]. Or use hash map for the last pair.

---

## 15.6 When to Use Two Pointers vs Sliding Window

- **Sorted array, pair/subarray sum** → opposite ends or same-direction two pointers.
- **Contiguous subarray satisfying condition (e.g., sum ≤ K, at most K distinct)** → sliding window (Chapter 16).
- **Cycle / middle in linked list** → fast & slow.

---

## 15.7 Complexity

Typically **O(n)** or **O(n log n)** if sort is needed (e.g., three sum). **Space:** O(1) for the pointers; O(log n) or O(n) for sort.

---

## Practice Exercises

**E1.** Two Sum II (sorted) — opposite ends.

**E2.** Container With Most Water — opposite ends; move the shorter line.

**E3.** 3Sum — sort + one index + two pointers.

**E4.** Trapping Rain Water — two pointers from ends or prefix/suffix max.

**E5.** Remove Duplicates from Sorted Array — same direction.

**E6.** Linked List Cycle I/II — fast & slow.

**E7.** Palindrome (string) — two pointers from both ends.

---

## Chapter Summary

| Pattern | Use |
|---------|-----|
| Opposite ends | Sorted two-sum, trapping water, container |
| Same direction | Remove duplicates, partition |
| Fast & slow | Cycle detection, middle of list |
| Three/four sum | Sort + one/two fixed + two pointers |

**Previous:** [Chapter 14 → Binary Search](14_binary_search.md) | **Next:** [Chapter 16 → Sliding Window](16_sliding_window.md)
