# Chapter 2: Linked Lists

> *"A linked list is an array that traded random access for O(1) insertions anywhere."*

---

## 2.1 What Is a Linked List?

A **linked list** is a sequence of **nodes**, where each node stores:
1. A **value** (data)
2. A **pointer** (reference) to the next node

Unlike arrays, linked list elements are **not contiguous in memory**. You can only reach element i by following i pointers from the head.

```
Array:
┌────┬────┬────┬────┬────┐
│ 10 │ 20 │ 30 │ 40 │ 50 │   ← contiguous memory
└────┴────┴────┴────┴────┘

Linked List:
┌────┬──┐    ┌────┬──┐    ┌────┬──┐    ┌────┬────┐
│ 10 │ ─┼───►│ 20 │ ─┼───►│ 30 │ ─┼───►│ 40 │None│
└────┴──┘    └────┴──┘    └────┴──┘    └────┴────┘
  head                                    tail
```

---

## 2.2 Types of Linked Lists

### Singly Linked List
Each node points to the next. Traversal: one direction only.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Doubly Linked List
Each node points to both next and previous. Traversal: both directions.

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

### Circular Linked List
The tail node's `next` points back to the head. Used in round-robin scheduling.

---

## 2.3 Full Implementation

```python
class LinkedList:
    """Singly linked list with all common operations."""

    def __init__(self):
        self.head = None
        self.size = 0

    # ── Building ──────────────────────────────────────────

    def append(self, val):
        """Add to end. O(n) — must traverse to tail."""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def prepend(self, val):
        """Add to front. O(1)."""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, val):
        """Insert at given index. O(n)."""
        if index == 0:
            self.prepend(val)
            return
        curr = self.head
        for _ in range(index - 1):
            if not curr:
                raise IndexError("Index out of range")
            curr = curr.next
        new_node = ListNode(val)
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    # ── Deleting ──────────────────────────────────────────

    def delete_val(self, val):
        """Delete first occurrence of val. O(n)."""
        if not self.head:
            return
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                self.size -= 1
                return
            curr = curr.next

    # ── Searching ─────────────────────────────────────────

    def search(self, val):
        """Find node with val. O(n)."""
        curr = self.head
        while curr:
            if curr.val == val:
                return curr
            curr = curr.next
        return None

    # ── Display ───────────────────────────────────────────

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

    def __repr__(self):
        return " → ".join(map(str, self.to_list())) + " → None"
```

---

## 2.4 The Essential Trick: The Dummy Node

When you might delete or insert at the head, a **dummy node** before the head eliminates special cases:

```python
def delete_val_clean(head, val):
    """With dummy node — no edge case for deleting head."""
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy

    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next

    return dummy.next  # new head (may have changed)
```

> **Interview Tip:** The dummy node pattern eliminates almost all edge cases in linked list problems. Use it by default.

---

## 2.5 Core Techniques

### Technique 1: Two Pointers (Fast & Slow)

A slow pointer moves 1 step at a time; a fast pointer moves 2. By the time fast reaches the end, slow is at the middle.

```
Initial: slow = fast = head
         1 → 2 → 3 → 4 → 5 → None

Step 1:  slow = 2,  fast = 3
Step 2:  slow = 3,  fast = 5
         fast.next = None → STOP
         slow is at node 3 (middle)
```

**Application 1: Find Middle of Linked List**
```python
def find_middle(head):
    """O(n) time, O(1) space."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle node
```

**Application 2: Detect Cycle (Floyd's Algorithm)**
```python
def has_cycle(head):
    """If there's a cycle, fast and slow will eventually meet."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

**Application 3: Find Cycle Start**
```python
def detect_cycle_start(head):
    """
    After slow and fast meet inside the cycle:
    Move one pointer to head. Both move at speed 1.
    They meet at the cycle entrance.

    Why? If cycle starts at position k from head, and
    the meeting point is at position m from cycle start,
    then k = L - m where L is cycle length. (Math proof omitted.)
    """
    slow = fast = head
    # Phase 1: detect meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle

    # Phase 2: find cycle entrance
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow  # cycle start
```

**Application 4: Find Kth Node from End**
```python
def kth_from_end(head, k):
    """Move fast k steps ahead. Then move both until fast hits end."""
    fast = slow = head
    for _ in range(k):
        if not fast:
            return None  # list shorter than k
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    return slow  # kth from end
```

---

### Technique 2: Reversing a Linked List

The most fundamental linked list operation. Every interview candidate must be able to code this from memory.

```
Before: 1 → 2 → 3 → 4 → None
After:  4 → 3 → 2 → 1 → None
```

**Iterative Reversal (O(n) time, O(1) space):**
```python
def reverse_list(head):
    prev = None
    curr = head

    while curr:
        next_node = curr.next   # 1. Save next
        curr.next = prev        # 2. Reverse pointer
        prev = curr             # 3. Move prev forward
        curr = next_node        # 4. Move curr forward

    return prev  # prev is now the new head
```

**Trace through:**
```
Initial: prev=None, curr=1

Step 1: next=2, 1.next=None, prev=1, curr=2
        None ← 1    2 → 3 → 4

Step 2: next=3, 2.next=1, prev=2, curr=3
        None ← 1 ← 2    3 → 4

Step 3: next=4, 3.next=2, prev=3, curr=4
        None ← 1 ← 2 ← 3    4

Step 4: next=None, 4.next=3, prev=4, curr=None
        None ← 1 ← 2 ← 3 ← 4

Return prev = 4 (new head)
```

**Recursive Reversal (O(n) time, O(n) space):**
```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head

    new_head = reverse_list_recursive(head.next)
    head.next.next = head   # make next node point back to current
    head.next = None        # cut current node's forward pointer
    return new_head
```

---

### Technique 3: Reverse a Sublist (positions m to n)

```python
def reverse_between(head, m, n):
    """Reverse nodes from position m to n (1-indexed)."""
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    # Move prev to node just before position m
    for _ in range(m - 1):
        prev = prev.next

    # curr is node at position m
    curr = prev.next

    # Reverse n - m times
    for _ in range(n - m):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next
```

---

### Technique 4: Merge Two Sorted Lists

```python
def merge_sorted(l1, l2):
    """O(m + n) time, O(1) space."""
    dummy = ListNode(0)
    curr = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next

    curr.next = l1 or l2  # attach remaining
    return dummy.next
```

---

## 2.6 Classic Problems, Fully Solved

### Problem 1: Palindrome Linked List
*Check if a singly linked list is a palindrome in O(n) time and O(1) space.*

```python
def is_palindrome(head):
    # Step 1: Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: Reverse second half
    prev = None
    curr = slow
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    right = prev  # head of reversed second half

    # Step 3: Compare both halves
    left = head
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True
```

---

### Problem 2: Remove Nth Node from End
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast hits end
    while fast:
        slow = slow.next
        fast = fast.next

    # slow is now just before the node to delete
    slow.next = slow.next.next
    return dummy.next
```

---

### Problem 3: Reorder List
*Reorder: L0 → L1 → … → Ln-1 → Ln into L0 → Ln → L1 → Ln-1 → L2 → …*

```python
def reorder_list(head):
    # Step 1: Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: Reverse second half
    prev, curr = None, slow.next
    slow.next = None  # cut list in half
    while curr:
        curr.next, prev, curr = prev, curr, curr.next
    second = prev

    # Step 3: Interleave first and reversed second half
    first = head
    while second:
        first.next, second.next = second, first.next
        first = first.next
        second = second.next
```

---

## 2.7 Complexity Summary

| Operation | Singly LL | Doubly LL | Array |
|-----------|-----------|-----------|-------|
| Access by index | O(n) | O(n) | O(1) |
| Search | O(n) | O(n) | O(n) |
| Insert at head | O(1) | O(1) | O(n) |
| Insert at tail | O(n) | O(1)* | O(1)* |
| Insert in middle | O(n) | O(n) | O(n) |
| Delete at head | O(1) | O(1) | O(n) |
| Delete at tail | O(n) | O(1)* | O(1)* |
| Delete in middle | O(n) | O(n) | O(n) |

*With tail pointer.

---

## Practice Exercises

### Easy
**E1.** Reverse a singly linked list iteratively. Return the new head.

**E2.** Delete a node given only a reference to that node (not the head). Assume it's not the tail.
<details>
<summary>Hint</summary>
Copy next node's value into current node, then skip next node: `node.val = node.next.val; node.next = node.next.next`
</details>

**E3.** Given a sorted linked list, remove all duplicate elements.

### Medium
**E4.** Given a linked list, determine if it has a cycle. Return True/False.

**E5.** Merge k sorted linked lists into one sorted list.
<details>
<summary>Hint</summary>
Use a min-heap of (value, node). Extract min, push its next. O(N log k) where N = total nodes.
</details>

**E6.** Given a linked list where each node has an additional pointer to a random node (or None), deep copy the list.
<details>
<summary>Hint</summary>
Two passes: first create all nodes storing old→new mapping. Second pass set next and random pointers.
</details>

**E7.** Rotate linked list to the right by k places.
<details>
<summary>Hint</summary>
Connect tail to head (make circular). New tail is at position (n - k%n - 1). Cut there.
</details>

### Hard
**E8.** Sort a linked list in O(n log n) time and O(1) space.
<details>
<summary>Hint</summary>
Bottom-up merge sort on linked lists. Merge sublists of size 1, then 2, then 4... No recursion stack needed. O(n log n) time, O(1) space.
</details>

**E9.** Given a linked list and value x, partition it so all nodes less than x come before nodes ≥ x, while preserving relative order.
<details>
<summary>Hint</summary>
Maintain two lists: "less" and "greater_equal". Connect them at the end.
</details>

---

## Chapter Summary

| Technique | Use Case |
|-----------|----------|
| Dummy node | Avoids head edge cases in deletion/insertion |
| Fast & slow pointers | Middle, cycle detection, kth from end |
| Reverse in-place | Palindrome check, reorder list |
| Two-pass | Nth from end, deep copy |
| Merge sorted lists | Merge k sorted lists (with heap) |

**Previous:** [Chapter 1 → Arrays & Strings](01_arrays_strings.md) | **Next:** [Chapter 3 → Stacks](03_stacks.md)
