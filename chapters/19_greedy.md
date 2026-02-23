# Chapter 19: Greedy Algorithms

> *"Greedy: make the best local choice and never look back. When it works, it's fast and simple."*

---

## 19.1 Why Greedy Matters

**Greedy** algorithms make a **locally optimal** choice at each step, hoping the result is globally optimal. They work when the problem has **greedy choice property** (a global optimum can be reached by a series of local choices) and **optimal substructure** (optimal solution contains optimal solutions to subproblems). Classic uses: interval scheduling, merge intervals, jump game, Huffman (conceptual). When greedy fails (e.g., coin change with arbitrary denominations), use DP. Proving correctness often uses **exchange argument**: show that replacing the greedy choice with another leads to a solution that is no better.

---

## 19.2 Greedy Choice Property

At each step, there exists an optimal solution that includes the greedy choice. Example: **Activity selection** — choose the activity that ends earliest; then an optimal schedule can include it and then solve the subproblem over activities that start after it finishes.

---

## 19.3 Interval Pattern

**Merge overlapping intervals:** Sort by start (or end). Merge: if current overlaps last in result (current.start <= result[-1].end), extend result's end; else append current.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

**Insert interval:** Add new interval, then merge (or do one pass: insert in order by start, then merge).

**Meeting rooms II (min rooms):** Sort all starts and ends; sweep: +1 on start, -1 on end; max concurrent = max of running sum. Or: sort by start, min-heap of end times; for each meeting, pop all ended, push current end, max size of heap = rooms needed.

**Non-overlapping intervals (erase minimum to make non-overlapping):** Equivalent to "max number of non-overlapping intervals" — sort by end; take greedily (next must have start >= last end). Answer = n - count.

---

## 19.4 Activity Selection / Interval Scheduling

Given activities [start, end], pick maximum number of non-overlapping activities. **Greedy:** Sort by end time; take first; then take next that starts >= last end. Correct by exchange argument.

---

## 19.5 Jump Game

**Jump Game I:** Can you reach the last index? Greedy: maintain `furthest` you can reach; for each i, if i <= furthest: furthest = max(furthest, i + nums[i]). Return furthest >= n-1.

**Jump Game II:** Minimum jumps. Greedy: at each step, from current range [left, right], next range is [right+1, max(i + nums[i]) for i in range(left, right+1)]; jump count += 1; repeat until right >= n-1.

---

## 19.6 Huffman Encoding (Conceptual)

Build a binary tree so that frequent symbols have short codes. Greedy: repeatedly merge the two smallest frequency nodes. Result: prefix-free code; optimal for symbol-by-symbol encoding.

---

## 19.7 When Greedy Fails

**Coin change:** With coins [1, 3, 4] and amount 6, greedy (largest first) gives 4+1+1 = 3 coins; optimal is 3+3 = 2. So use DP.

**Rule of thumb:** If you need to "reconsider" past choices, greedy usually doesn't work — think DP or backtracking.

---

## 19.8 Proving Correctness

- **Exchange argument:** Show that swapping/adjusting the greedy choice in any optimal solution doesn't improve it (or keeps optimality).
- **Induction:** First step is correct; after making the greedy choice, the remaining problem is a smaller instance of the same type.

---

## Practice Exercises

**E1.** Merge Intervals — sort by start, merge.

**E2.** Insert Interval — insert then merge (or one pass).

**E3.** Non-overlapping Intervals — max non-overlapping (sort by end); answer = n - count.

**E4.** Meeting Rooms II — sweep line or min-heap of end times.

**E5.** Jump Game — furthest reachable.

**E6.** Jump Game II — BFS-like ranges or greedy steps.

**E7.** Task Scheduler — schedule most frequent first with cooldown (or formula: (max_count-1)*(n+1) + num_max).

**E8.** Partition Labels — greedy: extend partition until last occurrence of all chars in partition is included.

**E9.** Gas Station — if total gas >= total cost, solution exists; start from index where running deficit is minimum (or first index from which you can complete a full circle).

---

## Chapter Summary

| Pattern | Use |
|---------|-----|
| Intervals | Merge, insert, max non-overlapping, meeting rooms |
| Sort then greedy | Activity selection, intervals |
| Reachability | Jump game, gas station |
| Exchange argument | Proving correctness |

**Previous:** [Chapter 18 → Dynamic Programming](18_dynamic_programming.md) | **Next:** [Chapter 20 → Divide & Conquer](20_divide_and_conquer.md)
