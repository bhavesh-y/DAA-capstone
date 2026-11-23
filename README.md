# Project 4: Social Network Connection and Recommendation Analysis

> **Design and Analysis of Algorithms (DAA) Capstone Project**  
> **Topic:** Graph Traversal Algorithms (BFS & DFS), Shortest Paths, Mutual Connections, and Recommendation Systems.

---

## 📌 Problem Statement

Develop a social network analysis system in which users are represented as vertices and their connections as edges. 
- Implement **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** to explore user connections.
- Identify **mutual connections** between users.
- Determine the **shortest connection path** and degrees of separation between two users.
- Implement a **recommendation system** ("People You May Know") based on mutual connection counts and similarity metrics.
- **Analyse the performance** of graph traversal algorithms across networks of different sizes ($|V|$ and $|E|$).

---

## 🚀 Key Features Implemented

1. **Graph Representation**:
   - Built using an **Adjacency List** (`collections.defaultdict(set)`), offering optimal $O(1)$ edge lookups and efficient traversal.
   - Vertices represent individual users; undirected edges represent mutual friendships.

2. **Breadth-First Search (BFS)**:
   - Explores connections layer-by-layer (FIFO queue via `collections.deque`).
   - Grouping users by **Degrees of Separation** (1st-degree direct friends, 2nd-degree friends of friends, etc.).
   - Guarantees the **unweighted shortest path** between any two users with path reconstruction.

3. **Depth-First Search (DFS)**:
   - Explores paths as deep as possible before backtracking (LIFO stack).
   - Iterative implementation to guard against recursion limits on large networks.
   - Identifies **Connected Components / Communities** (disjoint user clusters).

4. **Mutual Connections**:
   - Calculates the intersection set $N(u) \cap N(v)$ of friends between two users in $O(\min(\text{deg}(u), \text{deg}(v)))$ time.

5. **Friend Recommendation ("People You May Know")**:
   - Evaluates 2nd-degree connections (friends of friends who are not yet connected).
   - Computes candidate ranking based on:
     - **Common Neighbors Count**: $|N(u) \cap N(v)|$
     - **Jaccard Similarity Coefficient**: $\frac{|N(u) \cap N(v)|}{|N(u) \cup N(v)|}$

6. **Performance & Complexity Benchmarking**:
   - Benchmarks BFS and DFS execution times on synthetic networks of varying sizes:
     - 100 nodes (400 edges)
     - 500 nodes (2,000 edges)
     - 1,000 nodes (4,000 edges)
     - 2,500 nodes (10,000 edges)
     - 5,000 nodes (20,000 edges)
   - Compares empirical runtime against theoretical complexities.

---

## ⏱️ Algorithm Complexity Analysis

| Algorithm / Operation | Time Complexity | Space Complexity | Description |
| :--- | :---: | :---: | :--- |
| **Add User / Edge** | $O(1)$ | $O(1)$ | Hash set addition in adjacency list |
| **BFS Traversal** | $O(V + E)$ | $O(V)$ | Enqueues each vertex once, scans each edge twice |
| **DFS Traversal** | $O(V + E)$ | $O(V)$ | Pushes each vertex once, scans each edge twice |
| **Shortest Path (BFS)** | $O(V + E)$ | $O(V)$ | Early exit on target reached + path backtrack |
| **Mutual Connections** | $O(\min(\text{deg}(u), \text{deg}(v)))$ | $O(\min(\text{deg}(u), \text{deg}(v)))$ | Set intersection of neighbor lists |
| **Friend Recommendation** | $O(\text{deg}(u) \times \overline{\text{deg}})$ | $O(V)$ | Explores 2nd-degree neighborhood |
| **Connected Components** | $O(V + E)$ | $O(V)$ | Full graph sweep using DFS |

---

## 🛠️ How to Run

### Requirements
- Python 3.7+ (No external packages required; uses standard libraries: `collections`, `time`, `random`).

### Execution
Run the script directly using Python:

```bash
python3 social_network_analysis.py
```

---

## 📊 Sample Output

```text
================================================================================
PROJECT 4: SOCIAL NETWORK CONNECTION AND RECOMMENDATION ANALYSIS
================================================================================

[+] Network Initialized Successfully!
    Total Users (Vertices |V|): 13
    Total Friendships (Edges |E|): 16
    Users: Alice, Bob, Charlie, Diana, Edward, Frank, Grace, Henry, Ivy, Jack, Xavier, Yusuf, Zara

--- 1. Breadth-First Search (BFS) Exploration from 'Alice' ---
    BFS Visit Order (Level-by-Level): Alice -> Bob -> Charlie -> Diana -> Edward -> Frank -> Grace -> Henry -> Ivy -> Jack
    - Degree 1 Connections (Direct): Bob, Charlie, Diana
    - Degree 2 Connections (2-hop): Edward, Frank, Grace
    - Degree 3 Connections (3-hop): Henry, Ivy

--- 2. Depth-First Search (DFS) Exploration from 'Alice' ---
    DFS Visit Order (Depth-First): Alice -> Bob -> Charlie -> Frank -> Diana -> Grace -> Ivy -> Edward -> Henry -> Jack

--- 3. Network Clusters / Connected Communities (via DFS) ---
    Total Disconnected Communities: 2
    - Community 1 (10 members): Alice, Bob, Charlie, Diana, Edward, Frank, Grace, Henry, Ivy, Jack
    - Community 2 (3 members): Xavier, Yusuf, Zara

--- 4. Shortest Connection Path between 'Alice' and 'Jack' (BFS) ---
    Shortest Path: Alice -> Charlie -> Frank -> Henry -> Jack
    Degrees of Separation: 4 hop(s)

--- Shortest Path between Disconnected Users 'Alice' and 'Zara' ---
    Result: No path exists! They belong to different connected components.

--- 5. Mutual Connections Identification ---
    Direct Friends of Alice: Bob, Charlie, Diana
    Direct Friends of Edward: Bob, Frank, Henry
    Mutual Friends between Alice and Edward: Bob

--- 6. Friend Recommendation Analysis for 'Alice' ('People You May Know') ---
    Rank #1: Frank
            Mutual Friends Count : 2
            Mutual Friends List  : Charlie, Diana
            Jaccard Similarity   : 0.333
    Rank #2: Grace
            Mutual Friends Count : 1
            Mutual Friends List  : Diana
            Jaccard Similarity   : 0.2
    Rank #3: Edward
            Mutual Friends Count : 1
            Mutual Friends List  : Bob
            Jaccard Similarity   : 0.2

================================================================================
PERFORMANCE ANALYSIS: GRAPH TRAVERSAL ALGORITHMS (BFS vs DFS)
================================================================================
Nodes (|V|)  | Edges (|E|)  | BFS Avg Time (ms)  | DFS Avg Time (ms)  | Faster Alg
--------------------------------------------------------------------------------
100          | 400          | 0.0731             | 0.1050             | BFS (30.3% faster)
500          | 2000         | 0.3587             | 0.4927             | BFS (27.2% faster)
1000         | 4000         | 0.7173             | 0.9777             | BFS (26.6% faster)
2500         | 10000        | 1.7930             | 2.4127             | BFS (25.7% faster)
5000         | 20000        | 3.6463             | 4.8446             | BFS (24.7% faster)
--------------------------------------------------------------------------------

[Algorithm Complexity & Empirical Summary]
1. Theoretical Time Complexity for both BFS & DFS: O(V + E)
   - In an adjacency list, every vertex is enqueued/pushed once -> O(V)
   - Every edge is inspected twice (undirected graph) -> O(E)
2. Empirical Observation:
   - Both algorithms scale linearly with graph size (V + E).
   - BFS uses deque.popleft() (FIFO queue), while DFS uses list.pop() (LIFO stack).
   - BFS finds unweighted shortest path with minimal degrees of separation.
   - DFS is ideal for connectivity, cycle detection, and finding topological groupings.
================================================================================
```

---

## 📁 Repository Structure

```
DAA capstone/
├── social_network_analysis.py   # Core implementation, algorithms & benchmarking
└── README.md                    # Project documentation, complexity analysis & guide
```
