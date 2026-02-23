# Chapter 9: Tries (Prefix Trees)

> *"A trie trades space for time: shared prefixes are stored once. That's why autocomplete and word search love it."*

---

## 9.1 Why Tries Matter

A **trie** (prefix tree) stores a set of strings so that **prefix lookups** and **startsWith** are fast. Each path from root to a node represents a prefix; a boolean (or count) on a node can mark end-of-word. Compared to a hash set of strings: trie supports "all keys with prefix P" in O(length of P + number of results) and shares storage for common prefixes. Interviews use tries for autocomplete, word search in a grid, IP routing (longest prefix match), and "add/search word" with wildcards.

---

## 9.2 Structure

- **Root** has no character; children are first characters of strings.
- Each **node** has:
  - A map (or array of size 26 for lowercase letters): character → child node.
  - Optional: `is_end` (or `count`) to mark end of a word.
- **Path from root to a node** = prefix (or full word if `is_end`).

```
Strings: "cat", "car", "card", "care"

         root
        /    \
       c      ...
       |
       a
      / \
     t   r
    *   /|\
       t d e
       * * *
```

`*` = end of word.

---

## 9.3 Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._traverse(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._traverse(prefix) is not None

    def _traverse(self, s: str) -> TrieNode | None:
        node = self.root
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
```

**Insert:** O(m), m = length of word. **Search / startsWith:** O(m). **Space:** O(total characters in all words), with sharing.

---

## 9.4 Compact Representation (Optional)

For lowercase letters only, use a fixed-size list of 26 instead of a dict (faster, less flexible):

```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

def idx(c):
    return ord(c) - ord('a')

# In insert/search: use node.children[idx(c)]
```

---

## 9.5 Applications

### Autocomplete / all keys with prefix

From the node for the prefix, DFS (or BFS) and collect all nodes where `is_end` is True. Optionally limit to top K by frequency (store count in node and use a heap).

### Word search in grid

Put all dictionary words in a trie. For each cell, DFS in the grid and simultaneously walk the trie. When you reach a node with `is_end`, record the word. Prune when the current path is not a prefix of any word (trie has no child for current cell letter).

### Design Add and Search Words Data Structure

Search supports a wildcard `.` (any character). For `.`, try all children; recurse for each. Use the same trie; only search logic changes.

```python
def search_with_wildcard(node, word, i):
    if i == len(word):
        return node.is_end
    c = word[i]
    if c == '.':
        return any(
            search_with_wildcard(node.children[ch], word, i + 1)
            for ch in node.children
        )
    if c not in node.children:
        return False
    return search_with_wildcard(node.children[c], word, i + 1)
```

### Longest common prefix

Insert all strings. Walk from root until a node has more than one child or is_end; the path so far is the common prefix.

---

## 9.6 Trie vs Hash Map

| Operation | Trie | Hash set |
|-----------|------|----------|
| Insert word | O(m) | O(m) |
| Exact search | O(m) | O(m) average |
| StartsWith(P) | O(\|P\|) | O(n) over all keys |
| All keys with prefix | O(\|P\| + k) | O(n) |
| Space | Shared prefixes | One copy per key |

Use a trie when you need **prefix** or **by-prefix** operations. Use a set when you only need exact membership.

---

## 9.7 Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(m) | O(m) per new path |
| Search / startsWith | O(m) | O(1) |
| All words with prefix | O(\|P\| + k) | O(1) extra |

m = word length; k = number of output words.

---

## 9.8 Gotchas

- **End marker:** Always set `is_end = True` on the last node of a word; otherwise "car" might not be distinguished from "cart" if you only check existence of path.
- **Empty string:** Decide if "" is a valid word; if so, mark `root.is_end` for it.
- **Delete:** To remove a word, unset `is_end` and optionally prune nodes that become useless (no children and not end of another word). Often not asked.

---

## Practice Exercises

### Easy

**E1.** Implement Trie (Prefix Tree) — insert, search, startsWith.

**E2.** Longest Common Prefix — insert all, walk while single child and not end.

### Medium

**E3.** Design Add and Search Words Data Structure — trie + wildcard search (recurse on all children for '.').

**E4.** Word Search II — grid + list of words. Put words in trie; DFS grid and walk trie; collect words at is_end.

**E5.** Replace Words — dictionary of roots; replace each word in sentence with shortest root that is a prefix. Trie of roots; for each word find shortest prefix in trie.

### Hard

**E6.** Word Squares — build trie by prefix and by "column prefix"; backtrack to form square.

**E7.** Palindrome Pairs — for each word, check if reverse of suffix/prefix is in trie (with special handling for palindromic remainder).

---

## Chapter Summary

| Pattern | Use Case |
|---------|----------|
| Insert / search / startsWith | Dictionary, autocomplete |
| DFS from prefix node | All keys with prefix |
| Trie + grid DFS | Word search in grid |
| Wildcard in search | Try all children for '.' |

**Previous:** [Chapter 8 → Graphs](08_graphs.md) | **Next:** [Chapter 10 → Union-Find](10_union_find.md)
