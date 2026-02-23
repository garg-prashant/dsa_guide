# Chapter 27: Reservoir Sampling & Randomized Algorithms

> *"How do you pick a random sample when you don't know how many items there are? Reservoir sampling."*

---

## 27.1 Why Reservoir Sampling Matters

You have a **stream** of items (unknown length n). You want to choose **k** items **uniformly at random** — each subset of size k should be equally likely. You can't store everything (stream is huge) and you don't know n in advance. **Reservoir sampling** does this in **one pass**, O(n) time, using only **O(k)** space. It appears in big-data and streaming systems. It also illustrates how a simple **random choice** per item gives a global uniform sample.

---

## 27.2 Algorithm: Reservoir Sampling (k = 1)

**Goal:** One item chosen uniformly at random from the stream.

**Algorithm:**

1. Store the first item as the current **candidate**.
2. For the i-th item (i = 2, 3, …): with probability **1/i**, **replace** the candidate with this item; otherwise keep the candidate.
3. After the stream ends, the candidate is a **uniform random** item.

**Why it works:** For stream of length n, the probability that the j-th item (1 ≤ j ≤ n) is the final candidate equals 1/n. (Proof: chosen when we see it with prob 1/j, and never replaced by j+1 with prob (1 − 1/(j+1)), …, by n with prob (1 − 1/n). Product telescopes to 1/n.)

---

## 27.3 Algorithm: Reservoir Sampling (general k)

**Goal:** k items chosen uniformly at random from the stream (without replacement).

**Algorithm:**

1. **Reservoir:** Store the first k items in an array `reservoir[0..k-1]`.
2. For the i-th item (i = k+1, k+2, …): with probability **k/i**, **replace** a **random** position in the reservoir (uniform from 0 to k−1) with this item; otherwise do nothing.
3. After the stream ends, the reservoir is a **uniform random k-subset**.

**Why it works:** For any set S of k indices in {1..n}, the probability that the final reservoir is exactly the items at S is 1 / C(n,k). So each k-subset is equally likely.

```python
import random

def reservoir_sample(stream, k):
    """One pass; stream is an iterable of unknown length. Returns list of k items."""
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randrange(i + 1)  # 0..i inclusive
            if j < k:
                reservoir[j] = item
    return reservoir

# Example: sample 3 from range(100)
sample = reservoir_sample(iter(range(100)), 3)
```

---

## 27.4 Weighted Reservoir Sampling (Conceptual)

If each item has a **weight** w_i and we want to sample so that the probability of selecting item i is proportional to w_i, we use **weighted reservoir sampling**: when processing item i, replace a random reservoir entry with probability proportional to w_i and the current total weight. (Algorithm details: e.g. replace with probability k * w_i / W_i where W_i is cumulative weight so far.)

---

## 27.5 Other Randomized Ideas

- **Randomized quicksort:** Pick random pivot; expected O(n log n). Reduces worst-case chance.
- **Hash-based sampling:** Hash each item to [0,1); keep the k smallest hashes. Gives approximate uniform sample and can be parallelized.
- **Bloom filter:** Probabilistic set membership; false positives possible, no false negatives. (See references for details.)

---

## 27.6 Complexity

| Problem | Time | Space |
|---------|------|-------|
| Reservoir k from stream (length n) | O(n) | O(k) |
| Weighted reservoir | O(n) | O(k) |

---

## Practice Exercises

**E1.** Prove that for k=1 reservoir sampling, the probability that the j-th stream item is the final candidate is 1/n (n = stream length).

**E2.** How would you sample **with replacement** (k draws, each draw uniform over all items) in one pass with O(k) space? (Hint: store indices or items and update probabilities.)

**E3.** (Application) You have a stream of log lines. How do you output a random subset of 100 lines in one pass?

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Reservoir (k=1) | Keep one candidate; replace with prob 1/i for i-th item |
| Reservoir (k) | Keep k; for i-th item (i>k), replace random slot with prob k/i |
| Result | Uniform random k-subset; one pass, O(k) space |
| Use | Streaming, big data, unknown n |

**Previous:** [Chapter 26 → Skip List](26_skip_list.md) | **Next:** [Chapter 28 → Sweep Line](28_sweep_line.md)
