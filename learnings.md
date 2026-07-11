# Learnings

## Key Concepts

**PageRank is an eigenvector problem** — the scores are the dominant eigenvector of the Google matrix. Power iteration finds it by repeatedly multiplying the matrix by a vector until it stops changing.

**Columns must sum to 1, not rows** — the transition matrix is column-stochastic. Column j represents outgoing links from node j. Each column sums to 1 so probability is conserved at each step.

**Adjacency matrix direction matters** — storing `matrix[to][from] = 1` (column = source) makes column normalization natural. Storing it the other way requires a transpose before normalization, which causes subtle bugs.

**Dangling nodes leak probability** — a page with no outgoing links absorbs probability but never releases it. The fix redistributes its weight uniformly across all nodes in the Google matrix, not in the transition matrix.

**Teleportation prevents traps** — without the `(1-d)/n` term, a surfer caught in a strongly connected component would never escape. Teleportation ensures every node is reachable from every other node, guaranteeing convergence.

## Bugs Fixed

- **Transition matrix direction wrong**: normalized rows instead of columns — scores diverged from NetworkX entirely
- **Dangling node detected but never used**: built the dangling list but applied `d × T + teleport` only, ignoring the fix — dangling nodes inflated scores of unconnected pages
- **adjacency convention mismatch**: `add_link(from, to)` set `matrix[from][to]` but transition normalization treated columns as sources — reversed to `matrix[to][from]`

## Surprises

- Node 3 (no incoming links) scored 0.0375 in NetworkX but 0.2138 in the broken version — dangling node correction had a huge effect
- Power iteration converges in under 100 iterations for most graphs despite the 1000 iteration limit
- A symmetric graph (0→1→2→0) gives equal PageRank to all nodes regardless of damping factor
- Higher damping makes distributions less uniform — more extreme differences between high and low ranked pages