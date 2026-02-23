# Chapter 22: String Algorithms

> *"String matching goes from naive O(nm) to linear with KMP or Rabin-Karp. Know one well; know when to use which."*

---

## 22.1 Why String Algorithms Matter

Interviews ask **pattern matching** (find/count occurrences of pattern in text), **longest palindromic substring**, and **rolling hash** for duplicate detection. Naive matching is O(nm). **KMP** gives O(n + m) for single pattern; **Rabin-Karp** gives O(n + m) average with rolling hash and supports multiple patterns. **Z-algorithm** and **Manacher's** are useful for specific problems. This chapter gives you enough to choose and implement the right tool.

---

## 22.2 Naive Pattern Matching

Try every starting position in text; at each position, compare pattern character by character. **Time:** O(nm). **Space:** O(1).

```python
def naive_match(text, pattern):
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            return i
    return -1
```

---

## 22.3 KMP (Knuth-Morris-Pratt)

**Idea:** Build a **failure/lps** array for the pattern: lps[i] = longest proper prefix of pattern[:i+1] that is also a suffix. When a mismatch occurs, shift pattern by (matched_length - lps[matched_length-1]) instead of 1.

**Build lps:** For each position i, if pattern[i] == pattern[len], len++; lps[i]=len; else if len>0, len=lps[len-1]; else lps[i]=0.

**Search:** Two pointers: i in text, j in pattern. Match: i++, j++. Mismatch: if j>0, j=lps[j-1]; else i++.

```python
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    lps = [0] * m
    length = 0
    for i in range(1, m):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]
        if pattern[i] == pattern[length]:
            length += 1
        lps[i] = length

    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - m
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1
```

**Time:** O(n + m). **Space:** O(m).

---

## 22.4 Rabin-Karp (Rolling Hash)

**Idea:** Compute hash of pattern; compute hash of each length-m window in text. If hashes match, confirm with direct comparison (to handle collisions). Use a **rolling hash**: subtract contribution of leaving character, multiply by base, add new character. Mod a large prime to keep values small.

```python
def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    base, mod = 26, 10**9 + 7
    def hash_str(s):
        h = 0
        for c in s:
            h = (h * base + (ord(c) - ord('a'))) % mod
        return h
    target = hash_str(pattern)
    cur = hash_str(text[:m])
    if cur == target and text[:m] == pattern:
        return 0
    mult = pow(base, m - 1, mod)
    for i in range(m, n):
        cur = (cur - (ord(text[i-m]) - ord('a')) * mult) % mod
        cur = (cur * base + (ord(text[i]) - ord('a'))) % mod
        if cur == target and text[i-m+1:i+1] == pattern:
            return i - m + 1
    return -1
```

**Time:** O(n + m) average; worst O(nm) with bad collisions. **Use for:** Multiple patterns (hash each; check window hash against set), duplicate substring detection.

---

## 22.5 Z-Algorithm

**Z[i]** = length of longest substring starting at i that matches a prefix of the string. Used for: find all occurrences of pattern in text (concat pattern + "$" + text, then Z values at text positions); longest prefix that is also suffix. **Time:** O(n + m) to build Z array.

---

## 22.6 Manacher's Algorithm (Longest Palindromic Substring)

Finds longest palindromic substring in **O(n)**. Idea: maintain "center" and "right boundary" of the current rightmost palindrome; use symmetry to reuse information. For interviews, **expand around center** (O(n²)) is often acceptable: for each index (and between indices), expand while symmetric. Manacher gives O(n) and is good to know for "optimal" answers.

```python
def longest_palindrome_expand(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]
    best = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1) if i + 1 < len(s) else ""
        best = max(best, odd, even, key=len)
    return best
```

---

## 22.7 When to Use Which

| Need | Algorithm |
|------|-----------|
| Single pattern, linear time | KMP |
| Multiple patterns, duplicate substrings | Rabin-Karp |
| All occurrences, Z values | Z-algorithm |
| Longest palindromic substring | Expand O(n²) or Manacher O(n) |

---

## 22.8 Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Naive | O(nm) | O(1) |
| KMP | O(n + m) | O(m) |
| Rabin-Karp | O(n + m) avg | O(1) |
| Expand center | O(n²) | O(1) |
| Manacher | O(n) | O(n) |

---

## Practice Exercises

**E1.** Implement strStr() — KMP or Rabin-Karp.

**E2.** Repeated DNA Sequences — rolling hash of length-10 window; count occurrences.

**E3.** Longest Palindromic Substring — expand around center or Manacher.

**E4.** Shortest Palindrome — find longest prefix that is a palindrome (e.g., KMP on s + "#" + reverse(s)); append reverse of the rest.

**E5.** Longest Duplicate Substring — binary search on length; Rabin-Karp to check if any length-L substring appears twice.

---

## Chapter Summary

| Algorithm | Use |
|-----------|-----|
| KMP | Single pattern, failure function |
| Rabin-Karp | Rolling hash, multiple patterns |
| Z | All occurrences, prefix-suffix |
| Expand / Manacher | Longest palindromic substring |

**Previous:** [Chapter 21 → Graph Algorithms](21_graph_algorithms.md) | **Next:** [Chapter 23 → Bit Manipulation](23_bit_manipulation.md)
