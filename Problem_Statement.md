# Day 5 — PageRank Algorithm Using Linear Algebra

## Problem Statement
Implement Google's PageRank algorithm from scratch using only the custom Matrix library built on Day 1. No NetworkX. No numpy. Pure linear algebra.

## Core Questions
- How does a search engine decide which pages are important?
- How do you handle pages with no outgoing links (dangling nodes)?
- How does the damping factor model random surfing behavior?

## Requirements
- WebGraph class to represent directed link structure as an adjacency matrix
- Transition matrix with column-wise normalization
- Google matrix with damping factor and dangling node correction
- Power iteration to find the dominant eigenvector (PageRank scores)
- Results must match NetworkX within tolerance of 0.05