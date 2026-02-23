# Chapter 23: Bit Manipulation

> *"Bits are the smallest unit of data. Flipping, masking, and shifting unlock constant-space tricks."*

---

## 23.1 Why Bit Manipulation Matters

Many interview problems can be solved with **bitwise operations**: **AND**, **OR**, **XOR**, **NOT**, **left/right shift**. Uses include: check/set/clear/toggle a bit, power-of-2 checks, "single number" (XOR), subset enumeration with bitmasks, and low-level optimizations. Python integers are arbitrary-precision; for fixed-width (e.g., 32-bit), mask with `0xFFFFFFFF` or use `n & ((1 << 32) - 1)`.

---

## 23.2 Operators (Python)

| Operator | Symbol | Example |
|----------|--------|---------|
| AND | `&` | `5 & 3` → 1 |
| OR | `\|` | `5 \| 3` → 7 |
| XOR | `^` | `5 ^ 3` → 6 |
| NOT | `~` | `~5` → -6 (two's complement) |
| Left shift | `<<` | `1 << 3` → 8 |
| Right shift | `>>` | `8 >> 2` → 2 |

**XOR properties:** a ^ a = 0; a ^ 0 = a; a ^ b ^ b = a. **Use:** find unique element when all others appear twice; swap without temp (a^=b; b^=a; a^=b).

---

## 23.3 Common Tricks

**Check if bit i is set:** `(n >> i) & 1` or `n & (1 << i) != 0`.

**Set bit i:** `n | (1 << i)`.

**Clear bit i:** `n & ~(1 << i)`.

**Toggle bit i:** `n ^ (1 << i)`.

**Clear rightmost set bit:** `n & (n - 1)`. Example: 12 (1100) → 8 (1000). **Power of 2:** `n > 0 and (n & (n - 1)) == 0`.

**Get rightmost set bit:** `n & (-n)` (lowbit). Used in Fenwick tree (Chapter 12).

**Count set bits (popcount):** `bin(n).count('1')` or while n: count += n & 1; n >>= 1. Or `n & (n-1)` in a loop (drops lowest set bit each time).

---

## 23.4 Single Number / Missing Number

**Single Number I:** Every element appears twice except one. XOR all: duplicates cancel, result is the single one. **Single Number II:** One element once, others three times — use bits: for each bit position, count mod 3; that bit of the answer is 1 if count % 3 == 1.

**Missing number in [0..n]:** XOR all indices and all values; same as XOR of [0..n] and the array; result is the missing number. Or sum: n*(n+1)//2 - sum(arr).

---

## 23.5 Subsets with Bitmasks

For a set of n elements, each subset corresponds to a number 0..2^n-1: bit i = 1 means element i is in the subset.

```python
def subsets_bitmask(arr):
    n = len(arr)
    out = []
    for mask in range(1 << n):
        out.append([arr[i] for i in range(n) if (mask >> i) & 1])
    return out
```

---

## 23.6 Signed vs Unsigned, Overflow

In Python, integers don't overflow. In C/Java, 32-bit signed: range -2^31..2^31-1; right shift of negative is implementation-defined (arithmetic vs logical). For "32-bit unsigned" in Python: use `n & 0xFFFFFFFF` and treat result as unsigned for display (or convert to signed if needed: if >= 2^31, subtract 2^32).

---

## 23.7 Complexity

Most bit tricks are **O(1)** or **O(number of bits)** (e.g., O(32)). Subset enumeration is O(2^n × n).

---

## Practice Exercises

**E1.** Single Number — XOR all.

**E2.** Number of 1 Bits (Hamming weight) — n & (n-1) in loop or built-in.

**E3.** Missing Number — XOR or sum.

**E4.** Power of Two — n > 0 and (n & (n-1)) == 0.

**E5.** Reverse Bits — extract bit by bit and build result.

**E6.** Subsets — bitmask 0 to 2^n-1.

**E7.** Single Number II — count bits mod 3.

**E8.** Maximum XOR of Two Numbers in an Array — trie of bits (MSB first) or try each pair (if small).

---

## Chapter Summary

| Trick | Use |
|-------|-----|
| n & (n-1) | Clear rightmost set bit; power of 2 check |
| n & (-n) | Lowbit (Fenwick) |
| XOR | Single number, missing number, swap |
| Bitmask | Enumerate subsets |

**Previous:** [Chapter 22 → String Algorithms](22_string_algorithms.md) | **Next:** [Chapter 24 → Math & Number Theory](24_math_number_theory.md)
