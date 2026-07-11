# Approach

## Core Design — WebGraph

`WebGraph` stores the link structure as an adjacency matrix where columns represent source nodes:

add_link(from, to) → matrix[to][from] = 1

This column-as-source convention means each column j holds the outgoing links of node j. Normalizing columns to sum to 1 gives the transition matrix directly.

The transition matrix represents random surfing — if you're on page j, you follow one of its outgoing links with equal probability:

add_link(from, to) → matrix[to][from] = 1

This column-as-source convention means each column j holds the outgoing links of node j. Normalizing columns to sum to 1 gives the transition matrix directly.

The transition matrix represents random surfing — if you're on page j, you follow one of its outgoing links with equal probability:

T[i][j] = 1 / (number of outgoing links from j)   if j has links
= 0 otherwise

## Core Design — PageRank

`PageRank` builds the Google matrix and finds its dominant eigenvector via power iteration.

**Google Matrix:**

G = d × T + dangling_fix + teleport


Three components:
- `d × T` — follow links with probability d (damping factor, default 0.85)
- `dangling_fix` — redistribute dangling node weight evenly across all nodes
- `teleport = (1-d)/n` — random jump to any page with probability 1-d

**Power Iteration:**

Start: r = [1/n, 1/n, ..., 1/n]
Loop:  r_new = G @ r
Stop:  when sum(|r_new - r|) < 1e-9

The vector converges to the stationary distribution of the Markov chain — the PageRank scores.

## Dangling Node Handling

A dangling node has no outgoing links — its column in the transition matrix is all zeros. Without correction, probability mass leaks out of the system and scores don't sum to 1.

Fix: detect zero columns, then add `d / n` to every entry in that column in the Google matrix. This redistributes the dangling node's weight evenly across all pages.

## Damping Factor

Models the real behavior of a web surfer:
- With probability d (0.85): follow a link on the current page
- With probability 1-d (0.15): jump to a completely random page

Higher damping → surfer follows links more → distribution deviates further from uniform → pages with many inbound links rank higher.

