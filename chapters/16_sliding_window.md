# Chapter 16: Sliding Window

> *"A sliding window keeps a contiguous segment under the lens. Expand and shrink to satisfy the condition — often O(n)."*

---

## 16.1 Why Sliding Windows Matter

**Sliding window** maintains a **contiguous subarray** (or substring) and updates it by **expanding** or **shrinking** one end. Used for "longest substring with at most K distinct", "minimum window substring", "max sum of size K", etc. Two flavors: **fixed size** (window length K) and **variable size** (expand until condition holds, then shrink from the left). Often combined with a **frequency map** or **deque** (see **Chapter 4** for deque-based max/min in window). This chapter focuses on the expand/shrink and frequency-map patterns; deque for max/min is in Chapter 4.

---

## 16.2 Fixed-Size Window

Window of length K; slide by one each time. **Idea:** When the window slides right, one element enters and one leaves — update the window state in O(1) instead of recomputing from scratch.

**Example:** Max sum of any contiguous subarray of size K = 3.  
arr = [2, 1, 5, 1, 3, 2]

```
Window [2,1,5] → sum = 8
Slide: drop 2, add 1 → [1,5,1] sum = 8 - 2 + 1 = 7
Slide: drop 1, add 3 → [5,1,3] sum = 7 - 1 + 3 = 9  ← best
Slide: drop 5, add 2 → [1,3,2] sum = 9 - 5 + 2 = 6
Answer: 9
```

```python
def max_sum_subarray(arr, k):
    cur = sum(arr[:k])
    best = cur
    for i in range(k, len(arr)):
        cur += arr[i] - arr[i - k]
        best = max(best, cur)
    return best
```

---

## 16.3 Variable-Size Window (Expand / Shrink)

**Template:**  
- **Right pointer** expands the window (add element).  
- When the window **violates** the condition, **left pointer** shrinks (remove element) until the condition holds again.  
- After each step, the window is valid; update the answer (e.g., min length, max length).

### Worked Example: Longest Substring Without Repeating Characters

**Problem:** Find length of longest substring with all distinct characters.  
s = "a b c a b c b b" (spaces for clarity).

```
Step:  right  char   window (left..right)   freq           valid?  best
  1     0     'a'   [a]                    {a:1}         yes     1
  2     1     'b'   [ab]                   {a:1,b:1}      yes     2
  3     2     'c'   [abc]                  {a:1,b:1,c:1} yes     3
  4     3     'a'   [abca]                 {a:2,...}     no → shrink
        shrink: left=0 remove 'a' → left=1, [bca]        yes     3
  5     4     'b'   [bcab]                {b:2,...}     no → shrink
        shrink: left=1,2,3 → [ab] then left=4 [b]        yes     3
  ... continue; answer = 3 (e.g. "abc" or "bca" or "cab")
```

**Longest substring with at most K distinct characters:**

```python
def longest_k_distinct(s, k):
    from collections import defaultdict
    freq = defaultdict(int)
    left = 0
    best = 0
    for right in range(len(s)):
        freq[s[right]] += 1
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Longest substring without repeating characters:** Same idea; condition is "no character count > 1". Shrink while any count > 1.

```python
def length_of_longest_substring(s):
    from collections import defaultdict
    freq = defaultdict(int)
    left = 0
    best = 0
    for right in range(len(s)):
        freq[s[right]] += 1
        while any(freq[c] > 1 for c in freq):
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

## 16.4 Minimum Window Substring

Find smallest substring of `s` that contains every character of `t` (with required frequencies). **Expand** right until the window has all chars; **shrink** left while the window still has all; record minimum length and substring.

```python
def min_window(s, t):
    from collections import Counter
    need = Counter(t)
    have = 0
    required = len(need)
    freq = {}
    left = 0
    best_len, best_start = float('inf'), 0
    for right in range(len(s)):
        c = s[right]
        freq[c] = freq.get(c, 0) + 1
        if c in need and freq[c] == need[c]:
            have += 1
        while have == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            c = s[left]
            freq[c] -= 1
            if c in need and freq[c] < need[c]:
                have -= 1
            left += 1
    return s[best_start:best_start + best_len] if best_len != float('inf') else ""
```

---

## 16.5 Window with Frequency Map — Summary

- **Expand:** right++; update freq[s[right]].
- **Shrink:** while condition broken: update freq[s[left]], left++.
- **Answer:** update after each valid window (e.g., max length, min length, count).

---

## 16.6 Deque for Max/Min in Window (Reference)

For "max in every sliding window of size K", use a **monotonic deque** that stores indices; front = max in current window. See **Chapter 4**.

---

## 16.7 When to Use Sliding Window

- **Contiguous subarray/substring** + **condition on the segment** (sum, distinct count, contains pattern) → try sliding window.
- **Fixed size** → single loop with add one, drop one.
- **Variable size** → expand right, shrink left until valid; track best.

---

## 16.8 Complexity

Usually **O(n)**. Space O(k) or O(1) for frequency map (bounded alphabet).

---

## Practice Exercises

**E1.** Maximum Average Subarray I (fixed size K) — sliding sum.

**E2.** Longest Substring Without Repeating Characters — variable window, freq map.

**E3.** Minimum Window Substring — variable window, contain all chars of t.

**E4.** Subarray Product Less Than K — variable window; shrink while product >= K.

**E5.** Max Consecutive Ones III — at most K zeros; variable window.

**E6.** Sliding Window Maximum — monotonic deque (Chapter 4).

---

## Chapter Summary

| Type | Use |
|------|-----|
| Fixed size | Max sum, fixed K |
| Variable + freq map | At most K distinct, no repeat, min window |
| Deque | Max/min per window (Ch 4) |

**Previous:** [Chapter 15 → Two Pointers](15_two_pointers.md) | **Next:** [Chapter 17 → Recursion & Backtracking](17_recursion_backtracking.md)
