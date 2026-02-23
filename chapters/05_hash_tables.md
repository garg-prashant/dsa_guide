# Chapter 5: Hash Tables

> *"A hash table is a cheat code. It turns O(n) lookups into O(1)."*

---

## 5.1 What Is a Hash Table?

A **hash table** (also called hash map or dictionary) stores key-value pairs. It uses a **hash function** to compute an index into an array of buckets, where the value is stored.

```
Key: "apple"
        ↓
   hash("apple") = 42 (some number)
        ↓
   42 % bucket_count = 2
        ↓
   buckets[2] → ("apple", 100)
```

The magic is that we can **find any key in O(1) average time** — we just compute the hash and go directly to the bucket.

---

## 5.2 How Hashing Works

A good hash function has two properties:
1. **Deterministic** — same input always gives same output
2. **Uniform distribution** — minimizes collisions

```python
# Python's built-in hash function
hash("hello")    # some integer, consistent within one session
hash(42)         # 42 (integers hash to themselves usually)
hash((1, 2, 3))  # tuples are hashable (immutable)
# hash([1,2,3]) → TypeError! Lists are not hashable (mutable)
```

> **Key Rule:** Only **immutable** objects can be dictionary keys in Python. Strings, numbers, tuples ✓. Lists, dicts, sets ✗.

---

## 5.3 Collision Handling

Two keys can hash to the same bucket (collision). Two main strategies:

### 1. Chaining
Each bucket holds a linked list. Multiple keys in the same bucket are stored as a list.

```
buckets[2] → [("apple", 100)] → [("grape", 200)] → None
```

Average O(1) with good hash function; worst case O(n) if all keys collide.

### 2. Open Addressing (Linear Probing)
If bucket i is occupied, try i+1, i+2, ... until empty.

Python's `dict` uses a variant of open addressing with a more sophisticated probing sequence.

---

## 5.4 Python's Dict and Set

```python
# Dict — key/value pairs
d = {}
d["name"] = "Alice"
d["age"] = 30
print(d["name"])         # "Alice"
print(d.get("city", "Unknown"))  # "Unknown" (default if missing)
print("age" in d)        # True
del d["age"]

# Iterate over dict
for key in d:            # keys
    print(key)
for val in d.values():   # values
    print(val)
for k, v in d.items():   # key-value pairs
    print(k, v)

# Dict comprehension
squares = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4, 3:9, 4:16}

# defaultdict — no KeyError for missing keys
from collections import defaultdict
word_count = defaultdict(int)       # default value: 0
word_count["hello"] += 1
char_lists = defaultdict(list)      # default value: []
char_lists["a"].append(1)

# Counter — frequency counting
from collections import Counter
c = Counter("banana")               # Counter({'a':3, 'n':2, 'b':1})
c.most_common(2)                    # [('a', 3), ('n', 2)]

# Set — keys only, no values
s = {1, 2, 3}
s.add(4)
s.remove(2)
3 in s          # True  (O(1))
s1 & s2         # intersection
s1 | s2         # union
s1 - s2         # difference
s1 ^ s2         # symmetric difference
```

---

## 5.5 Core Patterns

### Pattern 1: Frequency Counter

Count how often each element appears.

```python
from collections import Counter

def top_k_frequent(nums, k):
    """Return the k most frequent elements. O(n log k)."""
    count = Counter(nums)
    # nlargest is O(n log k) — more efficient than sorting all
    return [num for num, _ in count.most_common(k)]

print(top_k_frequent([1,1,1,2,2,3], k=2))  # [1, 2]
```

**Bucket Sort approach for O(n):**
```python
def top_k_frequent_linear(nums, k):
    count = Counter(nums)
    # Bucket i contains all numbers with frequency i
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
```

---

### Pattern 2: Two-Sum Lookup

Store **elements seen so far** (value → index). For each new element `x`, check if `target - x` is already in the map; if yes, you have a pair.

**Worked example:** nums = [2, 7, 11, 15], target = 9.

```
i=0, num=2: complement=7, 7 not in seen → seen = {2: 0}
i=1, num=7: complement=2, 2 in seen → return [seen[2], 1] = [0, 1]
```

One pass, O(n) time, O(n) space.

```python
def two_sum(nums, target):
    """O(n) time, O(n) space."""
    seen = {}  # value → index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

---

### Pattern 3: Grouping by Key

Transform each element into a canonical form (its "key"), then group.

```python
from collections import defaultdict

def group_anagrams(strs):
    """Group strings that are anagrams of each other. O(n·k log k)."""
    groups = defaultdict(list)

    for s in strs:
        key = tuple(sorted(s))  # canonical form: sorted characters
        groups[key].append(s)

    return list(groups.values())

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

### Pattern 4: Hashing for Caching (Memoization)

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    """With memoization, O(n) time, O(n) space."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Manual memoization with dict
def fibonacci_manual(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_manual(n-1, memo) + fibonacci_manual(n-2, memo)
    return memo[n]
```

---

## 5.6 Classic Problems, Fully Solved

### Problem 1: Longest Consecutive Sequence

*Given an unsorted array, find the length of the longest consecutive sequence in O(n).*

**Key Insight:** Only start counting from the beginning of a sequence (where n-1 is not in the set).

```python
def longest_consecutive(nums):
    """O(n) time, O(n) space."""
    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start counting at the beginning of a sequence
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            max_length = max(max_length, length)

    return max_length

print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # 4 (1,2,3,4)
```

---

### Problem 2: Valid Sudoku

```python
def is_valid_sudoku(board):
    """O(1) time (fixed 9×9 board), O(1) space."""
    rows = defaultdict(set)
    cols = defaultdict(set)
    boxes = defaultdict(set)  # key: (row//3, col//3)

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue
            box_key = (r // 3, c // 3)
            if (val in rows[r] or val in cols[c] or val in boxes[box_key]):
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_key].add(val)

    return True
```

---

### Problem 3: Subarray Sum Equals K

```python
def subarray_sum(nums, k):
    """Count subarrays summing to k. O(n) time, O(n) space."""
    count = 0
    prefix_sum = 0
    freq = defaultdict(int)
    freq[0] = 1  # empty subarray has sum 0

    for num in nums:
        prefix_sum += num
        # If prefix_sum - k exists, those subarrays sum to k
        count += freq[prefix_sum - k]
        freq[prefix_sum] += 1

    return count

print(subarray_sum([1, 1, 1], 2))  # 2
print(subarray_sum([1, 2, 3], 3))  # 2 ([1,2] and [3])
```

---

### Problem 4: LRU Cache (Hard — Classic Design Problem)

*Design a Least Recently Used cache with O(1) get and put.*

**Approach:** Hash map for O(1) lookup + doubly linked list for O(1) move-to-front.

```python
class DNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}           # key → node
        # Dummy head and tail for the doubly linked list
        self.head = DNode()       # most recently used side
        self.tail = DNode()       # least recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._move_to_front(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)
        else:
            node = DNode(key, value)
            self.cache[key] = node
            self._insert_at_front(node)
            if len(self.cache) > self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node):
        self._remove(node)
        self._insert_at_front(node)
```

---

## 5.7 Complexity Summary

| Operation | Average Case | Worst Case |
|-----------|-------------|-----------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Space | O(n) | O(n) |

> Worst case occurs when all keys hash to the same bucket. In practice, Python's dict is almost always O(1) due to its excellent hash function and load factor management.

---

## Practice Exercises

### Easy
**E1.** Given two arrays, return their intersection (elements in both). Handle duplicates.
<details>
<summary>Hint</summary>
Use Counter for both. For each element, take min(count1, count2).
</details>

**E2.** Given a string, find the first non-repeating character. Return its index or -1.
<details>
<summary>Hint</summary>
Two passes: first count frequencies, second find first char with frequency 1.
</details>

### Medium
**E3.** Given an unsorted array, find if there exist two distinct indices i, j such that `|arr[i] - arr[j]| ≤ t` and `|i - j| ≤ k`.
<details>
<summary>Hint</summary>
Sliding window with a sorted structure (SortedList) or bucket approach: bucket each number into bucket of size t+1.
</details>

**E4.** Design a data structure that supports: `insert(val)`, `remove(val)`, `getRandom()` — all in O(1).
<details>
<summary>Hint</summary>
Array for O(1) random access + hash map for O(1) lookup. For remove: swap with last element, update map, pop last.
</details>

**E5.** Given n pairs of parentheses, generate all valid combinations.
<details>
<summary>Hint</summary>
Backtracking. Track count of open and close parens used. Add '(' if open < n, add ')' if close < open.
</details>

### Hard
**E6.** Given a list of words and a pattern, find all words that match the pattern. Two words match if there's a bijection between them: `e.g., "mee" matches "abb" (m→a, e→b)`.
<details>
<summary>Hint</summary>
Normalize each word to a pattern by replacing first occurrences with 0, 1, 2... Compare normalized forms.
</details>

---

## Chapter Summary

| Pattern | Common Use | Data Structure |
|---------|-----------|----------------|
| Frequency count | Top K, anagram check | `Counter` / `defaultdict(int)` |
| Two-Sum lookup | Pair finding | `dict` (value → index) |
| Group by key | Anagram grouping | `defaultdict(list)` |
| Prefix sum + map | Subarray sum problems | `defaultdict(int)` |
| Ordered map | LRU, time-based operations | `dict` + doubly linked list |

**Previous:** [Chapter 4 → Queues](04_queues.md) | **Next:** [Chapter 6 → Trees](06_trees.md)
