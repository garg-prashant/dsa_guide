# Chapter 24: Math & Number Theory

> *"Interviews love GCD, modular arithmetic, and primes. A small toolkit covers most problems."*

---

## 24.1 Why Math and Number Theory Matter

Many problems are **numerical**: divisibility, GCD, modular arithmetic, primes, combinatorics. You don't need deep theory — **Euclidean algorithm**, **modular exponentiation**, **sieve for primes**, and **nCr with mod** cover a large fraction. This chapter gives you the code and the "when to use" so you're not stuck on "how do I compute inverse?" or "how do I count primes?".

---

## 24.2 Euclidean Algorithm (GCD)

**gcd(a, b) = gcd(b, a % b)** until b = 0; then gcd = a. **Time:** O(log min(a,b)).

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

# Or recursive
def gcd_r(a, b):
    return a if b == 0 else gcd_r(b, a % b)
```

**LCM(a, b) = a * b // gcd(a, b).**

**Extended Euclidean:** Finds x, y such that ax + by = gcd(a,b). Used for **modular inverse** below.

```python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y
```

**Modular inverse of a mod m** (when gcd(a,m)=1): solve ax ≡ 1 (mod m). Use extended gcd: x from extended_gcd(a, m) is the inverse (mod m). Or use **Fermat:** when m is prime, a^(-1) ≡ a^(m-2) (mod m).

---

## 24.3 Modular Arithmetic

- (a + b) mod m = ((a mod m) + (b mod m)) mod m
- (a - b) mod m = ((a mod m) - (b mod m) + m) mod m
- (a * b) mod m = ((a mod m) * (b mod m)) mod m
- **Modular exponentiation:** a^b mod m in O(log b) by squaring.

```python
def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result
```

**Modular inverse (Fermat, m prime):** inv(a) = a^(m-2) % m.

---

## 24.4 Prime Numbers

**Trial division (is n prime?):** Check divisors from 2 to sqrt(n). O(sqrt(n)).

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

**Sieve of Eratosthenes (primes up to n):** Mark multiples of each prime. O(n log log n).

```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]
```

**Count primes in [0..n]:** Run sieve; prefix sum of is_prime.

---

## 24.5 Combinatorics

**Factorial:** fact(n) = n!; with mod: precompute up to n. **nCr = n! / (r! (n-r)!).** With mod (m prime): precompute factorials and inverse factorials; nCr = fact[n] * inv_fact[r] * inv_fact[n-r] % m.

```python
def nCr_mod(n, r, mod):
    if r < 0 or r > n:
        return 0
    num = den = 1
    for i in range(r):
        num = num * (n - i) % mod
        den = den * (i + 1) % mod
    return num * pow(den, mod - 2, mod) % mod
```

**Trailing zeroes in n!:** Count of factor 5 = n//5 + n//25 + n//125 + ...

---

## 24.6 Common Problems

**Count Primes** — Sieve; return count.  
**Power of Three** — Check n > 0 and 3^max_power % n == 0 (or divide by 3 until 1).  
**Happy Number** — Repeatedly sum squares of digits; use set to detect cycle.  
**Factorial Trailing Zeroes** — Count factors of 5.  
**Excel Sheet Column Number** — Base-26: result = result*26 + (ord(c)-ord('A')+1).

---

## 24.7 When to Use Math vs Simulation

- **Divisibility, GCD, LCM** → Euclidean.  
- **Large powers mod m** → Modular exponentiation.  
- **Primes in range** → Sieve.  
- **Ways to choose / arrange** → Combinatorics (factorial, nCr).  
- **Digit / number property** → Often simulation (happy number) or formula (trailing zeroes).

---

## Practice Exercises

**E1.** Count Primes — Sieve of Eratosthenes.

**E2.** Power of Three — Check 3^19 (or similar) divisible by n; or loop divide.

**E3.** Happy Number — Sum of squares of digits; cycle detection.

**E4.** Factorial Trailing Zeroes — Count 5s.

**E5.** Excel Sheet Column Number — Base-26.

**E6.** Modular multiplicative inverse — Extended GCD or Fermat.

**E7.** Unique Paths (m×n grid, only right/down) — (m+n-2) choose (n-1).

---

## Chapter Summary

| Topic | Tool |
|-------|------|
| GCD / LCM | Euclidean algorithm |
| Modular inverse | Extended GCD or Fermat (prime mod) |
| a^b mod m | Modular exponentiation |
| Primes in range | Sieve of Eratosthenes |
| nCr mod m | Factorial + inverse factorial |

**Previous:** [Chapter 23 → Bit Manipulation](23_bit_manipulation.md) | **Next:** [Chapter 25 → B-Trees & B+ Trees](25_btrees.md) (Part IV — Advanced)
