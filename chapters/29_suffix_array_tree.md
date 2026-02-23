# Chapter 29: Suffix Array & Suffix Tree

> *"To search for any substring quickly, index all suffixes. Suffix array and suffix tree do that."*

---

## 29.1 Why Suffix Array and Suffix Tree Matter

**Substring search** in a long string T: "Does pattern P appear in T?" Naive: O(|T| |P|). With a **suffix array** or **suffix tree** we build an index over T once (O(|T|) or O(|T| log |T|)), then each query "does P appear?" is **O(|P| + log |T|)** or O(|P|). They also enable **longest common substring** of two strings, **longest repeated substring**, and many string problems in bioinformatics and text search. **Suffix array** is simpler and space-efficient; **suffix tree** is more powerful but heavier.

---

## 29.2 Suffix Array

**Definition:** Sort all **suffixes** of T lexicographically. The **suffix array** SA[0..n-1] is the array of **starting indices** of these sorted suffixes (n = |T|).

**Example:** T = "banana", n = 6. Suffixes: "banana"(0), "anana"(1), "nana"(2), "ana"(3), "na"(4), "a"(5). Sorted: "a"(5), "ana"(3), "anana"(1), "banana"(0), "na"(4), "nana"(2). So **SA = [5, 3, 1, 0, 4, 2]**.

```
Sorted suffixes:
  5: a
  3: ana
  1: anana
  0: banana
  4: na
  2: nana
```

**Build:** O(n log n) by sorting suffixes (e.g. doubling / prefix-doubling), or O(n) with SA-IS or similar. Often implemented with **radix sort** on ranks.

---

## 29.3 LCP Array (Longest Common Prefix)

**LCP[i]** = length of the longest common prefix of SA[i] and SA[i-1]. So LCP[0] is often undefined or 0.

**Use:** Many substring and repeat problems use SA + LCP. E.g. **longest repeated substring** = max over LCP[i]. **Build LCP from SA:** O(n) with Kasai's algorithm.

```python
def build_lcp(T, SA):
    """T is the string, SA is suffix array. Returns LCP array."""
    n = len(T)
    rank = [0] * n
    for i in range(n):
        rank[SA[i]] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] == 0:
            h = 0
            continue
        j = SA[rank[i] - 1]
        while i + h < n and j + h < n and T[i + h] == T[j + h]:
            h += 1
        lcp[rank[i]] = h
        if h > 0:
            h -= 1
    return lcp
```

---

## 29.4 Substring Search with Suffix Array

**Query:** Does pattern P appear in T?  
**Binary search** on SA: compare P with the suffix at SA[mid]. If P is a prefix of that suffix, found. If P < suffix, search left; else search right. **Time:** O(|P| log |T|). With LCP and extra structures, O(|P| + log |T|).

---

## 29.5 Longest Common Substring of Two Strings

**Idea:** Build combined string T = A + '#' + B (#' not in A or B). Build SA and LCP. The longest common substring corresponds to a maximum LCP over pairs of suffixes that start in different parts (one in A, one in B). Sweep LCP and check that SA[i] and SA[i-1] are in different parts; take max LCP. **Time:** O(|A| + |B|).

---

## 29.6 Suffix Tree (Conceptual)

A **suffix tree** of T is a **trie** (or compact trie) of all suffixes of T. Each leaf corresponds to one suffix (store starting index). Each edge is labeled with a substring; labels are stored as (start, length) to keep size O(n).

**Properties:**
- Substring search: walk from root following P; if we can complete P, it appears in T. O(|P|).
- Build: O(n) with **Ukkonen's algorithm** (online, linear time). Implementation is complex.
- Space: O(n) with proper edge representation.

**When to use:** Suffix **array** + LCP is usually enough and easier to code. Use **suffix tree** when you need more (e.g. many distinct substring operations, or when a library provides it).

---

## 29.7 Comparison

| Aspect | Suffix Array | Suffix Tree |
|--------|---------------|-------------|
| Space | O(n) | O(n) |
| Build | O(n log n) or O(n) | O(n) (Ukkonen) |
| Substring search | O(|P| + log n) | O(|P|) |
| Implementation | Moderate | Hard |
| LCP / repeats | SA + LCP array | Natural from tree |

---

## Practice Exercises

**E1.** Given T and SA, implement binary search to check if pattern P exists in T.

**E2.** Using SA and LCP, how do you find the **longest repeated substring** of T? (Answer: max LCP[i].)

**E3.** (Conceptual) How would you count the number of distinct substrings of T using the suffix array? (Hint: total substrings = n(n+1)/2 minus sum of LCP[i].)

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Suffix array | Sorted indices of suffixes; build O(n log n), search O(|P| log n) |
| LCP array | Common prefix length of adjacent suffixes in SA; repeats, LCS |
| Suffix tree | Trie of suffixes; O(n) build, O(|P|) search; harder to implement |
| Use | Substring search, longest common/repeated substring |

**Previous:** [Chapter 28 → Sweep Line](28_sweep_line.md) | **Next:** [Chapter 30 → Advanced Graph Algorithms](30_advanced_graphs.md)
