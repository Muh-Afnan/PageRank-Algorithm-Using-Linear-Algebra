# Day 5 — PageRank Algorithm Using Linear Algebra

Google's PageRank algorithm implemented from scratch using the custom Matrix library from Day 1. No NetworkX. No numpy. Pure linear algebra.

## What It Does

- Models web pages as a directed graph stored as an adjacency matrix
- Builds a column-stochastic transition matrix from link structure
- Constructs the Google matrix with damping factor and dangling node correction
- Finds PageRank scores via power iteration
- Results match NetworkX within 0.05 tolerance

## Project Structure
pagerank_algorithm_using_linear_algebra/
├── src/
│   ├── graph.py          # WebGraph — adjacency and transition matrix
│   └── page_rank.py      # PageRank — Google matrix and power iteration
├── tests/
│   └── test_complete.py  # 8 tests
├── demo.py               # Example usage
├── problem_statement.md
├── approach.md
├── learnings.md
└── README.md

## Quick Start

```bash
python demo.py
```

## Core Classes

### WebGraph

```python
g = WebGraph(4)
g.add_link(0, 1)
g.add_link(1, 2)
g.add_link(2, 0)
g.add_link(3, 2)

T = g.transition_matrix()  # column-stochastic matrix
```

### PageRank

```python
pr = PageRank(damping=0.85)
scores = pr.fit(g)
ranking = pr.rank()  # sorted list of (node, score) tuples

# Example output:
# [(2, 0.3326), (0, 0.3202), (1, 0.3097), (3, 0.0375)]
```

## Tests

```bash
python -m pytest tests/test_complete.py
```
8 passed in 0.41s

| Test | What It Verifies |
|---|---|
| `test_transition_matrix_columns_sum_to_one` | Transition matrix is column-stochastic |
| `test_pagerank_sums_to_one` | Scores form a valid probability distribution |
| `test_pagerank_vector_non_negative` | All scores are non-negative |
| `test_dangling_node_handled` | Dangling nodes don't break the distribution |
| `test_damping_factor_effect` | Higher damping produces less uniform distribution |
| `test_convergence` | Same graph produces identical scores on repeated runs |
| `test_known_graph_ranking` | Most-linked node ranks highest |
| `test_matches_networkx` | Scores match NetworkX within 0.05 tolerance |

## Math

**Transition Matrix:**
T[i][j] = 1 / outdegree(j)   if j has outgoing links
= 0                   otherwise

**Google Matrix:**
G[i][j] = d × T[i][j] + d × dangling[j] / n + (1-d) / n

**Power Iteration:**
r = [1/n, ..., 1/n]
r = G @ r  (repeat until convergence)

## Key Insight

PageRank is an eigenvector problem. The scores are the dominant eigenvector of the Google matrix — the stationary distribution of a Markov chain that models a random web surfer. Power iteration finds it without ever explicitly computing eigenvalues.

## Dependencies

- `matrix_library` — Day 1 custom Matrix class (local dependency)
- No numpy, no networkx (networkx used only for test verification)