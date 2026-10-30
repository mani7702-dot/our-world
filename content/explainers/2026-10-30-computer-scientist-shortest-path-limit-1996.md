---
title: "How a computer scientist broke a 30-year-old math limit for finding the shortest path"
date: 2026-10-30
time: 12:05
image: assets/images/2026-10-30-computer-scientist-shortest-path-limit-1996.jpg
image_caption: "A network graph showing nodes connected by edges — the kind of structure that shortest-path algorithms navigate / Logan Essex / CC BY-SA 4.0 / Wikimedia Commons"
category: Science
read: 5 min
excerpt: "Every GPS app needs to find the quickest route between two places. But what if a computer had to calculate the shortest distance between every possible pair of points in a giant network? A new algorithm finally fixes a mathematical guarantee that had been stuck since 1996."
tags: science, computer science, algorithms, shortest path, graph theory, FOCS 2025, approximation
sample: false
for-grownups: "The All-Pairs Shortest Paths (APSP) problem asks for the shortest distance between every pair of vertices in a graph. A graph is a collection of points (vertices) joined by connections (edges) — think of cities connected by roads. Exact solutions are computationally expensive for large networks, so researchers use approximation algorithms that trade a little accuracy for a lot of speed. In 1996, Dor, Halperin, and Zwick (DHZ) developed a 2-approximation algorithm: it guarantees that estimated distances are never more than twice the true shortest distance. But DH Zwick's method only worked well when the two points were far apart; for nearby points, the guarantee could fail because sampled 'shortcut' vertices were too far from the direct route. Dr. Manoj Gupta at IIT Gandhinagar presented at FOCS 2025 a refinement using multi-scale sampling — organizing the network at several levels instead of one — so the 2-approximation guarantee now holds for close vertex pairs too, without increasing runtime complexity. Wikipedia's Shortest Path Problem article confirms that APSP is a fundamental graph-theory problem with well-known exact algorithms like Floyd-Warshall and Johnson's algorithm, and that approximation methods are valuable when networks are enormous. FOCS is recognized as one of the two top conferences in theoretical computer science, alongside STOC."
sources:
  - name: ScienceDaily — "A computer scientist breaks through a limit that stood since 1996"
    url: https://www.sciencedaily.com/releases/2026/10/261029072146.htm
  - name: FOCS 2025 — Gupta, "Improved 2-Approximate Shortest Paths for Close Vertex Pairs"
    url: https://doi.org/10.1109/FOCS50899.2025.00042
  - name: Wikipedia — Shortest Path Problem
    url: https://en.wikipedia.org/wiki/Shortest_path_problem
  - name: Wikipedia — Symposium on Foundations of Computer Science
    url: https://en.wikipedia.org/wiki/Symposium_on_Foundations_of_Computer_Science
---

# How a computer scientist broke a 30-year-old math limit for finding the shortest path

## The problem: every pair, every time

Every time you ask your phone for the fastest route, an algorithm called a **shortest-path search**
kicks in. It scans millions of streets and finds the quickest way from here to there. Easy enough.

But what if a computer had to do this for **every possible pair of places** in a giant network —
not just one trip, but all trips at once? That is what computer scientists call the **All-Pairs
Shortest Paths** problem. It is not just about maps. Social networks, internet cables, protein
structures, and brain neurons are all networks that need these calculations.

The problem is that as the network grows, the work grows **fast** — doubling the number of
points can multiply the effort by eight or more. So researchers look for **approximation
algorithms**: methods that give a pretty good answer quickly instead of a perfect answer
slowly.

## Step 1: The 1996 shortcut trick

In 1996, researchers Dor, Halperin, and Zwick came up with a clever idea. Instead of checking
every possible route between two points, they picked a **small set of "shortcut" points**
spread across the network. To estimate the distance between any two locations, the algorithm
asked: "How far is each location from the nearest shortcut point?" By comparing those shortcut
distances, it could guess the real distance without doing all the work.

The trick came with a **promise**: the guess would always be within **twice** the real distance.
If the true route was 10 kilometers, the estimate would be somewhere between 10 and 20. That
"twice as much at most" rule is called a **2-approximation** — a mathematical safety guarantee.

## Step 2: The hidden weakness (for close neighbors)

Here is the catch: the shortcut trick worked great when the two points were **far apart**,
like Delhi and Chennai in India. With a long journey, a shortcut point is likely to sit close
to the real path, so the estimate stays accurate.

But for points that are **close together**, the shortcut points could be nowhere near the
actual route. Imagine two neighborhoods in the same city. The nearest shortcut might be on
the other side of town, forcing the algorithm to estimate a five-step journey for a two-step
trip. That broke the "twice at most" promise — and it had been a puzzle for nearly three
decades.

## Step 3: The 2025 fix — sampling at multiple scales

Dr. Manoj Gupta from the Indian Institute of Technology Gandhinagar found a new way.
Instead of picking shortcuts at just one level, he organized the network at **multiple
scales** — like having a city map, a regional map, and a national map all at once. By checking
connections at each level, the algorithm could find better shortcut points for nearby pairs
without losing the speed guarantee.

The result: the 2-approximation promise now holds for **close pairs** as well as distant
ones, and the overall running time stays just as fast. It is not a new app on your phone
yet — the improvement lives in the math itself — but it strengthens the foundation that
engineers use to build the algorithms behind every route-planner and network tool.

## Try this at home

Draw a simple map of your neighborhood with at least six spots (your home, school, park,
store, friend's house, library). Connect pairs with lines of different lengths. Now try
to find the shortest route between every pair of spots. Start with a brute-force method
(check every path), then try the shortcut trick: mark two or three "hub" spots and estimate
longer distances by adding up hub-to-hub segments. Can you find a case where the shortcut
estimate is more than twice the real distance? That is the kind of puzzle Dr. Gupta solved!

## Fun Fact

The shortest-path problem is so fundamental that the **Floyd-Warshall algorithm** — which
solves it exactly for every pair of points — was described in papers as early as the 1960s.
But exact solutions become impossibly slow on massive networks like the entire internet,
which is why approximation methods like the one Dr. Gupta improved are so valuable. His
paper was presented at FOCS 2025, one of the two premier conferences in theoretical computer
science.

## Sources

1. ScienceDaily — "A computer scientist breaks through a limit that stood since 1996" (Oct 30, 2026): https://www.sciencedaily.com/releases/2026/10/261029072146.htm
2. FOCS 2025 — Gupta, "Improved 2-Approximate Shortest Paths for Close Vertex Pairs": https://doi.org/10.1109/FOCS50899.2025.00042
3. Wikipedia — Shortest Path Problem: https://en.wikipedia.org/wiki/Shortest_path_problem
4. Wikipedia — Symposium on Foundations of Computer Science: https://en.wikipedia.org/wiki/Symposium_on_Foundations_of_Computer_Science