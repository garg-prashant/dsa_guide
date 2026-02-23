# Chapter 28: Sweep Line

> *"Sweep a line across the plane; at each event, update your answer. Order is everything."*

---

## 28.1 Why Sweep Line Matters

Many **geometric** and **interval** problems become easier when we imagine a **sweep line** (vertical or horizontal) moving across the plane (or a timeline). We only care about **events** (e.g. segment start, segment end). Sort events, then process in order while maintaining a **data structure** for the current state (e.g. "active" intervals). This yields O(n log n) or O(n log n + k) algorithms for overlap counting, union area, closest pair (conceptual), and many interval problems. It's a standard technique in competitive programming and computational geometry.

---

## 28.2 The Pattern

1. **Identify events:** e.g. left edge of rectangle, right edge; start of interval, end of interval.
2. **Sort events** by position (x or time). Break ties (e.g. process "end" before "start" or vice versa depending on problem).
3. **Sweep:** For each event, update a structure (e.g. set of active intervals, segment tree, or counter) and update the answer.

---

## 28.3 Example: Merge Overlapping Intervals

**Problem:** Given intervals [start, end], merge all overlapping ones.

**Sweep:** Treat each interval as two events: (start, +1) and (end, -1). Sort by position; if tie, put end before start (so we don't count [1,2] and [2,3] as overlapping). Sweep and keep a **count** of open intervals. When count goes 0→1, start a new merged interval; when 1→0, close it.

```python
def merge_intervals(intervals):
    """Intervals: list of [start, end]. Merge overlapping. O(n log n)."""
    if not intervals:
        return []
    events = []
    for s, e in intervals:
        events.append((s, 1))   # open
        events.append((e, -1)) # close
    events.sort(key=lambda x: (x[0], -x[1]))  # same position: close before open
    merged = []
    count = 0
    start = None
    for pos, delta in events:
        if delta == 1:
            if count == 0:
                start = pos
            count += 1
        else:
            count -= 1
            if count == 0:
                merged.append([start, pos])
    return merged
```

---

## 28.4 Example: Number of Overlapping Intervals at Any Point

**Problem:** Maximum number of intervals that overlap at the same time.

**Events:** (position, +1) for start, (position, -1) for end. Sort; sweep and maintain `count`. Track max count. **Time:** O(n log n).

---

## 28.5 Example: Rectangle Area Union (Conceptual)

**Problem:** Union area of axis-aligned rectangles.

**Sweep:** Vertical line moving left to right. Events: x-coordinates of left and right edges. At each x, the "active" set of rectangles is a set of y-intervals. Compute the **total length** of the union of these y-intervals (e.g. with a segment tree or by merging intervals), multiply by the horizontal gap to next event, and add to area. **Time:** O(n² log n) naive; O(n log n) with segment tree for "union of intervals" length.

---

## 28.6 Example: Meeting Rooms II (Minimum Rooms)

**Problem:** Given meeting intervals, find the minimum number of rooms needed (max overlapping intervals).

**Same as 28.4:** Events (start, +1), (end, -1); sweep and take max of running count.

```python
def min_meeting_rooms(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], x[1]))  # end before start at same time
    count = 0
    best = 0
    for _, delta in events:
        count += delta
        best = max(best, count)
    return best
```

---

## 28.7 Tie-Breaking

Order of events at the **same position** matters. Examples:
- **Merge intervals:** At position x, if one interval ends and another starts, we usually want "end" first so we don't count them as overlapping: sort by (pos, -delta) so -1 comes before +1.
- **Max overlap:** Sometimes "start" first so we count both at the meeting point: sort by (pos, delta) or (pos, 1 then -1).

---

## 28.8 Complexity

| Problem | Time | Space |
|---------|------|-------|
| Merge intervals | O(n log n) | O(n) |
| Max overlapping intervals | O(n log n) | O(n) |
| Rectangle union area | O(n log n) with segment tree | O(n) |

---

## Practice Exercises

**E1.** Given intervals and a point q, count how many intervals contain q. (Sweep: events at each endpoint; at q, report current count — use events and binary search or sweep until q.)

**E2.** (LeetCode 218) Skyline: given rectangles, return the contour. Use sweep line with a multiset of heights.

**E3.** Given two sets of intervals A and B, compute the total length of overlap (each overlap counted once). Events: all endpoints; mark A vs B; sweep and maintain active A and active B; when both non-empty, add gap length.

---

## Chapter Summary

| Concept | Takeaway |
|--------|----------|
| Events | Start/end (or left/right); sort by position |
| Sweep | Process in order; maintain active set or count |
| Tie-break | Order of events at same position affects correctness |
| Use | Intervals, rectangles, geometry |

**Previous:** [Chapter 27 → Reservoir Sampling](27_reservoir_sampling.md) | **Next:** [Chapter 29 → Suffix Array & Suffix Tree](29_suffix_array_tree.md)
