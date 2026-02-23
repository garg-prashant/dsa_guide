# Chapter 3: Stacks

> *"A stack is the simplest data structure that thinks about the past — it only remembers what just happened."*

---

## 3.1 What Is a Stack?

A **stack** is a Last-In, First-Out (LIFO) data structure. Think of a stack of plates — you add to the top and remove from the top. The plate you added last is the first one you remove.

```
Push 1, Push 2, Push 3, Push 4

    ┌───┐  ← top
    │ 4 │
    ├───┤
    │ 3 │
    ├───┤
    │ 2 │
    ├───┤
    │ 1 │
    └───┘

Pop → 4, then 3, then 2, then 1
```

**Core operations:**
| Operation | Description | Time |
|-----------|-------------|------|
| `push(x)` | Add x to top | O(1) |
| `pop()` | Remove and return top | O(1) |
| `peek()` | View top without removing | O(1) |
| `is_empty()` | Check if stack is empty | O(1) |

---

## 3.2 Implementation in Python

Python's `list` is a perfect stack out of the box:

```python
stack = []

stack.append(1)   # push
stack.append(2)
stack.append(3)

print(stack[-1])  # peek → 3
stack.pop()       # pop → 3
stack.pop()       # pop → 2
print(stack)      # [1]
```

For a cleaner interface, you can wrap it:

```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
```

> **Interview Note:** Always use Python's built-in `list` as a stack. There's no need to implement your own unless explicitly asked. `collections.deque` is faster for large-scale use (O(1) pops from both ends without reallocation), but `list` is fine for interviews.

---

## 3.3 Why Stacks? The Recursive Intuition

Every recursive algorithm uses the **call stack** implicitly. A stack lets you simulate recursion iteratively — which sometimes gives you more control and avoids stack overflow.

```python
# Recursive DFS → uses call stack implicitly
def dfs_recursive(root):
    if not root:
        return
    print(root.val)
    dfs_recursive(root.left)
    dfs_recursive(root.right)

# Iterative DFS → uses explicit stack
def dfs_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
```

---

## 3.4 Core Technique: Monotonic Stack

This is one of the most powerful and frequently tested stack patterns.

A **monotonic stack** maintains elements in a strictly increasing or decreasing order. When a new element violates the ordering, we pop until the ordering is restored.

### Monotonic Decreasing Stack — Next Greater Element

**Problem:** For each element, find the first element to its right that is greater than it.

```
arr = [2, 1, 2, 4, 3, 1, 4, 2]

Process each element:
  i=0, val=2: stack=[], push (2,0)         → result[0]=?
  i=1, val=1: stack=[(2,0)], push (1,1)   → result[1]=?
  i=2, val=2: stack=[(2,0),(1,1)]
              1 < 2 → pop (1,1), result[1]=2
              2 = 2 → stop. push (2,2)
  i=3, val=4: stack=[(2,0),(2,2)]
              2 < 4 → pop (2,2), result[2]=4
              2 < 4 → pop (2,0), result[0]=4
              stack empty, push (4,3)
  i=4, val=3: 3 < 4, push (3,4)
  i=5, val=1: 1 < 3, push (1,5)
  i=6, val=4: pop (1,5) → result[5]=4
              pop (3,4) → result[4]=4
              4 = 4 → stop, push (4,6)
  i=7, val=2: 2 < 4, push (2,7)
  End: remaining in stack → result=-1

result = [4, 2, 4, -1, 4, 4, -1, -1]
```

```python
def next_greater(arr):
    """O(n) time, O(n) space."""
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices

    for i in range(n):
        # While current element is greater than element at stack top
        while stack and arr[i] > arr[stack[-1]]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)

    return result
```

> **Key Insight:** Each element is pushed once and popped once → **O(n) total**, not O(n²). This is the magic of the monotonic stack.

### Variant: Daily Temperatures (LeetCode 739)
*Given temperatures, return how many days until a warmer temperature.*

```python
def daily_temperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []  # indices

    for i in range(n):
        while stack and temps[i] > temps[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx  # days until warmer
        stack.append(i)

    return result

# Example:
print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

---

## 3.5 Largest Rectangle in Histogram

This is a hard problem that beautifully demonstrates the stack pattern. It appears frequently in FAANG interviews.

**Problem:** Given heights of histogram bars, find the area of the largest rectangle.

```
heights = [2, 1, 5, 6, 2, 3]

     6
   5 |
   | |
 2 | | | 3
 | | | | |
 | 1 | | 2 |
 ───────────
   0 1 2 3 4 5

Largest rectangle: 5×2 = 10 (bars at index 2 and 3, height 5)
```

**Approach:** Use a monotonic increasing stack of indices. When a bar is shorter than the stack top, the top bar can no longer extend rightward — compute its area.

```python
def largest_rectangle(heights):
    """O(n) time, O(n) space."""
    stack = []   # indices, heights are increasing
    max_area = 0
    heights = heights + [0]  # sentinel to flush stack at end

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area

print(largest_rectangle([2, 1, 5, 6, 2, 3]))  # 10
```

**Trace through (key steps):**
```
i=0, h=2: stack=[0]
i=1, h=1: heights[0]=2 > 1
          pop 0: height=2, width=1 (stack empty), area=2
          stack=[1]
i=2, h=5: stack=[1,2]
i=3, h=6: stack=[1,2,3]
i=4, h=2: heights[3]=6 > 2 → pop 3: height=6, width=4-2-1=1, area=6
          heights[2]=5 > 2 → pop 2: height=5, width=4-1-1=2, area=10 ← max
          heights[1]=1 < 2 → stop
          stack=[1,4]
...
```

---

## 3.6 Classic Problems, Fully Solved

### Problem 1: Valid Parentheses

```python
def is_valid(s):
    """O(n) time, O(n) space."""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)

    return not stack  # stack must be empty

print(is_valid("()[]{}"))   # True
print(is_valid("([)]"))     # False
print(is_valid("{[]}"))     # True
```

---

### Problem 2: Min Stack
*Design a stack that supports push, pop, top, and getMin in O(1).*

**Key Insight:** Track the minimum alongside the actual data. Each stack entry stores (value, min_at_this_level).

```python
class MinStack:
    def __init__(self):
        self._stack = []  # each entry: (value, current_min)

    def push(self, val):
        current_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, current_min))

    def pop(self):
        self._stack.pop()

    def top(self):
        return self._stack[-1][0]

    def get_min(self):
        return self._stack[-1][1]

# Example:
ms = MinStack()
ms.push(-2); ms.push(0); ms.push(-3)
print(ms.get_min())  # -3
ms.pop()
print(ms.top())      # 0
print(ms.get_min())  # -2
```

---

### Problem 3: Evaluate Reverse Polish Notation

```python
def eval_rpn(tokens):
    """O(n) time, O(n) space."""
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)  # truncate toward zero
    }

    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))

    return stack[0]

print(eval_rpn(["2","1","+","3","*"]))  # (2+1)*3 = 9
print(eval_rpn(["4","13","5","/","+"]))  # 4+(13/5) = 6
```

---

### Problem 4: Decode String (LeetCode 394)
*Decode "3[a2[c]]" → "accaccacc"*

```python
def decode_string(s):
    """O(n * max_k) time, O(n) space."""
    stack = []
    current_str = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # Save current state and start fresh
            stack.append((current_str, current_num))
            current_str = ""
            current_num = 0
        elif char == ']':
            # Pop saved state and repeat current string
            prev_str, repeat = stack.pop()
            current_str = prev_str + current_str * repeat
        else:
            current_str += char

    return current_str

print(decode_string("3[a]2[bc]"))    # aaabcbc
print(decode_string("3[a2[c]]"))     # accaccacc
```

---

## Practice Exercises

### Easy
**E1.** Implement a stack using two queues.
<details>
<summary>Hint</summary>
For each push, enqueue to queue1. For pop, move all but last element to queue2, return last, swap names. O(n) pop.
Alternatively: push O(n), pop O(1) — enqueue to empty queue, then move all from other queue behind it.
</details>

**E2.** Given a string with backspace characters (`#`), simulate typing and return the result.
```
"ab#c" → "ac", "a##c" → "c"
```

### Medium
**E3.** Given an array of integers and a number k, find the maximum in every sliding window of size k using a monotonic deque.
<details>
<summary>Hint</summary>
See Chapter 4 (Queues) for the full solution. Maintain a deque of indices with decreasing values. Front is always the window maximum.
</details>

**E4.** Implement a browser's forward/back navigation using two stacks.

**E5.** Given an expression string with `+`, `-`, `*`, `/` and parentheses, evaluate it.
<details>
<summary>Hint</summary>
Two stacks: one for numbers, one for operators. Process operators by precedence when a lower-precedence op is encountered.
</details>

### Hard
**E6.** Trapping Rainwater: Given an elevation map, compute how much water it can trap.
```
heights = [0,1,0,2,1,0,1,3,2,1,2,1]  → 6
```
<details>
<summary>Hint</summary>
Monotonic stack approach: when we find a "valley" (current > stack top), water fills the gap.
For each pop, water_level = min(current_height, left_wall_height) - bottom_height.
Alternatively, two pointer approach is O(1) space.
</details>

---

## Chapter Summary

| Pattern | Problem Type | Complexity |
|---------|-------------|-----------|
| Basic Stack | Balanced brackets, undo/redo | O(n) time, O(n) space |
| Monotonic Decreasing | Next greater element | O(n) time |
| Monotonic Increasing | Next smaller element | O(n) time |
| Stack + Min Tracking | Min/max stack | O(1) all operations |
| Two Stacks | Queue simulation, browser history | O(1) amortized |

**Previous:** [Chapter 2 → Linked Lists](02_linked_lists.md) | **Next:** [Chapter 4 → Queues & Deques](04_queues.md)
