# Path Optimization through a 2D Point Set

This project was developed as part of the semifinals of the German Informatics Competition 2022, where it received an exceptional score of 20/20 + 6 additional points.

## Overview

This project involves finding a path through a set of points in a two-dimensional Euclidean space. The path must satisfy the condition that the interior angle between any two consecutive segments of the path is always greater than 90 degrees. Additionally, the path should visit each point exactly once, minimizing the total distance traveled. The problem is a variation of the Traveling Salesman Problem (TSP), known for its NP-hard complexity, meaning it cannot be solved optimally in polynomial time.

## Problem Description

- **Objective**: Define a path through a 2D point set such that the interior angle between any two consecutive segments is always greater than 90 degrees and the total distance is minimized.
- **Constraints**: 
  - Each point must be visited exactly once.
  - The interior angle between any two consecutive segments must be greater than 90 degrees.
  - Start and end points are not identical.

## Solution Approach

### Adapting the TSP Algorithm

1. **Additional Theoretical Point**: To address the constraint of non-identical start and end points, a theoretical point with zero distance to all other points is added, serving as a common start and end point.
2. **Penalty Function**: A penalty function is introduced to handle the interior angle constraint, indicating the number of invalid angles in a route.

### Optimization Algorithms

- **k-opt Algorithms**: These involve removing k segments from the path and replacing them with new segments to create a new route. The process iterates to improve the path.
  - **2-opt Algorithm**: Removes two segments and reconnects the four points to reduce the path length.
  - **2h-opt Algorithm**: Extends 2-opt by also considering node shifts.
  - **3-opt Algorithm**: Removes three segments and considers seven possible new connections, offering better results but with increased computational time.

- **Lin-Kernighan Heuristic**: Dynamically adjusts the value of k to balance the quality of the solution and computational time. It iteratively builds alternating walks, adding nodes only if they do not negatively impact the overall gain.

- **Don't Look Optimization**: Prevents redundant checks of already examined segments, enhancing computational efficiency.

### Additional Techniques

- **Delaunay Triangulation**: Used for pre-selecting path segments.
- **POPMUSIC Metaheuristic**: A complex method not implemented due to its complexity.

### Linear Programming and Branch and Bound Approaches

These exact methods provide optimal solutions but are not practical for large datasets due to their extreme computational times.

## Usage

The code includes implementations of the 2-opt, 2h-opt, and Lin-Kernighan algorithms.

1. **2-opt Algorithm**: Implemented in `OpenTSP.java`
2. **Lin-Kernighan Heuristic**: Implemented in `basicLinKernighan.py`

For detailed algorithm behavior and optimization steps, please refer to the respective files and their comments within the code.

## Conclusion

This project provides a robust approach to solving a complex path optimization problem with constraints, leveraging advanced variations of traditional TSP algorithms and heuristics to achieve near-optimal solutions efficiently.

(For a more detailed documentation and analysis, view the included pdf file)
