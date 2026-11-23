"""
Social Network Connection and Recommendation Analysis
=====================================================
Course: Design and Analysis of Algorithms (DAA) Capstone Project 4
Problem Statement:
    Develop a social network analysis system in which users are represented as vertices
    and their connections as edges. Implement BFS and DFS to explore user connections,
    identify mutual connections, and determine the shortest connection path between two users.
    Analyse the performance of graph traversal algorithms for networks of different sizes.
"""

from collections import deque, defaultdict
import time
import random
from typing import Dict, List, Set, Tuple, Optional


class SocialNetwork:
    """
    Social Network Graph Representation using an Adjacency List.
    - Users: Vertices (V)
    - Friendships/Connections: Undirected Edges (E)
    """

    def __init__(self):
        # Adjacency list: user -> set of connected users
        self.adj_list: Dict[str, Set[str]] = defaultdict(set)

    def add_user(self, user: str) -> bool:
        """Adds a new user (vertex) to the social network."""
        user = str(user).strip()
        if not user:
            return False
        if user not in self.adj_list:
            self.adj_list[user] = set()
            return True
        return False

    def add_connection(self, user1: str, user2: str) -> bool:
        """
        Creates an undirected connection (edge) between user1 and user2.
        Automatically registers users if they are not already in the network.
        """
        user1, user2 = str(user1).strip(), str(user2).strip()
        if not user1 or not user2 or user1 == user2:
            return False

        self.add_user(user1)
        self.add_user(user2)
        self.adj_list[user1].add(user2)
        self.adj_list[user2].add(user1)
        return True

    def get_users(self) -> List[str]:
        """Returns all registered users in the network."""
        return list(self.adj_list.keys())

    def get_friends(self, user: str) -> Set[str]:
        """Returns the set of direct friends (1st-degree connections) of a user."""
        return self.adj_list.get(user, set()).copy()

    def num_users(self) -> int:
        """Returns total number of vertices |V|."""
        return len(self.adj_list)

    def num_connections(self) -> int:
        """Returns total number of unique undirected edges |E|."""
        return sum(len(neighbors) for neighbors in self.adj_list.values()) // 2

    # =========================================================================
    # 1. BREADTH-FIRST SEARCH (BFS)
    # =========================================================================
    def bfs_traversal(self, start_user: str) -> List[str]:
        """
        Explores the network level-by-level starting from start_user using BFS.
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_user not in self.adj_list:
            return []

        visited = {start_user}
        queue = deque([start_user])
        traversal_order = []

        while queue:
            current = queue.popleft()
            traversal_order.append(current)

            for neighbor in sorted(self.adj_list[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal_order

    def find_shortest_path(self, start_user: str, target_user: str) -> Tuple[Optional[List[str]], int]:
        """
        Finds the shortest connection path and degrees of separation between two users using BFS.
        Since edge weights are uniform (unweighted graph), BFS guarantees the shortest path.
        
        Returns:
            (path, distance): List of users representing the path, and degree of separation.
                              Returns (None, -1) if no path exists.
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_user not in self.adj_list or target_user not in self.adj_list:
            return None, -1

        if start_user == target_user:
            return [start_user], 0

        visited = {start_user}
        parent = {start_user: None}
        queue = deque([start_user])
        found = False

        while queue:
            current = queue.popleft()

            if current == target_user:
                found = True
                break

            for neighbor in self.adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        if not found:
            return None, -1

        # Reconstruct path
        path = []
        curr = target_user
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()

        degrees_of_separation = len(path) - 1
        return path, degrees_of_separation

    def get_connections_by_degrees(self, start_user: str, max_degree: int = 3) -> Dict[int, List[str]]:
        """
        Groups reachable users by their degree of separation from start_user using level-wise BFS.
        Degree 1: Direct friends
        Degree 2: Friends of friends
        ...
        """
        if start_user not in self.adj_list:
            return {}

        visited = {start_user}
        queue = deque([(start_user, 0)])
        degrees: Dict[int, List[str]] = defaultdict(list)

        while queue:
            current, dist = queue.popleft()

            if 0 < dist <= max_degree:
                degrees[dist].append(current)

            if dist < max_degree:
                for neighbor in sorted(self.adj_list[current]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))

        return dict(degrees)

    # =========================================================================
    # 2. DEPTH-FIRST SEARCH (DFS)
    # =========================================================================
    def dfs_traversal(self, start_user: str, iterative: bool = True) -> List[str]:
        """
        Explores connection paths as deep as possible before backtracking using DFS.
        Uses an iterative stack implementation to prevent recursion stack overflow on large networks.
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_user not in self.adj_list:
            return []

        if not iterative:
            # Recursive DFS
            visited = set()
            traversal_order = []

            def _dfs_rec(u: str):
                visited.add(u)
                traversal_order.append(u)
                for v in sorted(self.adj_list[u]):
                    if v not in visited:
                        _dfs_rec(v)

            _dfs_rec(start_user)
            return traversal_order

        # Iterative DFS using explicit stack
        visited = set()
        stack = [start_user]
        traversal_order = []

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                traversal_order.append(current)
                # Reverse sorted so that smaller alphanumeric names are explored first
                for neighbor in sorted(self.adj_list[current], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal_order

    def find_all_components(self) -> List[List[str]]:
        """
        Finds all isolated communities/connected components in the network using DFS.
        Time Complexity: O(V + E)
        """
        visited = set()
        components = []

        for user in self.adj_list:
            if user not in visited:
                comp = []
                stack = [user]
                visited.add(user)
                while stack:
                    curr = stack.pop()
                    comp.append(curr)
                    for nbr in self.adj_list[curr]:
                        if nbr not in visited:
                            visited.add(nbr)
                            stack.append(nbr)
                components.append(comp)

        return components

    # =========================================================================
    # 3. MUTUAL CONNECTIONS & RECOMMENDATION ANALYSIS
    # =========================================================================
    def get_mutual_connections(self, user1: str, user2: str) -> List[str]:
        """
        Finds all mutual friends between user1 and user2.
        Computed as the intersection of their neighbor sets: N(user1) ∩ N(user2)
        Time Complexity: O(min(deg(user1), deg(user2)))
        """
        friends1 = self.adj_list.get(user1, set())
        friends2 = self.adj_list.get(user2, set())
        return sorted(list(friends1 & friends2))

    def recommend_friends(self, user: str, top_k: int = 5) -> List[Dict]:
        """
        Recommends potential friends for a user ("People You May Know").
        
        Strategy (Collaborative Filtering / Common Neighbors Ranking):
        1. Explores 2nd-degree connections (friends of friends).
        2. Filters out the user themselves and existing direct friends.
        3. Ranks candidates by:
           - Number of mutual connections (Common Neighbors)
           - Jaccard Similarity Score: |N(u) ∩ N(v)| / |N(u) ∪ N(v)|
        
        Returns:
            List of recommendation dicts sorted by relevance.
        """
        if user not in self.adj_list:
            return []

        direct_friends = self.adj_list[user]
        candidate_scores: Dict[str, int] = defaultdict(int)

        # Count mutual friends for each 2nd-degree neighbor
        for friend in direct_friends:
            for candidate in self.adj_list[friend]:
                if candidate != user and candidate not in direct_friends:
                    candidate_scores[candidate] += 1

        recommendations = []
        user_deg = len(direct_friends)

        for candidate, mutual_count in candidate_scores.items():
            candidate_deg = len(self.adj_list[candidate])
            # Jaccard index = |A ∩ B| / |A ∪ B|
            union_size = user_deg + candidate_deg - mutual_count
            jaccard = (mutual_count / union_size) if union_size > 0 else 0.0

            mutual_list = self.get_mutual_connections(user, candidate)

            recommendations.append({
                "user": candidate,
                "mutual_count": mutual_count,
                "mutual_friends": mutual_list,
                "jaccard_similarity": round(jaccard, 3)
            })

        # Rank candidates primarily by mutual connection count, secondarily by Jaccard similarity
        recommendations.sort(
            key=lambda x: (x["mutual_count"], x["jaccard_similarity"]),
            reverse=True
        )

        return recommendations[:top_k]


# =============================================================================
# 4. PERFORMANCE ANALYSIS & BENCHMARKING
# =============================================================================

def generate_random_network(num_users: int, avg_friends: int = 6, seed: int = 42) -> SocialNetwork:
    """
    Generates a realistic synthetic social network with given number of users
    and approximate average degree using preferential attachment / random pairing.
    """
    random.seed(seed)
    net = SocialNetwork()
    users = [f"U{i}" for i in range(num_users)]

    for u in users:
        net.add_user(u)

    target_edges = (num_users * avg_friends) // 2
    edges_added = 0
    max_attempts = target_edges * 4
    attempts = 0

    while edges_added < target_edges and attempts < max_attempts:
        attempts += 1
        u1 = random.choice(users)
        u2 = random.choice(users)
        if u1 != u2 and u2 not in net.adj_list[u1]:
            net.add_connection(u1, u2)
            edges_added += 1

    return net


def run_performance_analysis(network_sizes: List[int] = None, runs_per_size: int = 5):
    """
    Benchmarks and compares the execution times of BFS vs DFS
    across varying network sizes (|V| and |E|).
    """
    if network_sizes is None:
        network_sizes = [100, 500, 1000, 2500, 5000]

    print("\n" + "=" * 80)
    print("PERFORMANCE ANALYSIS: GRAPH TRAVERSAL ALGORITHMS (BFS vs DFS)")
    print("=" * 80)
    print(f"{'Nodes (|V|)':<12} | {'Edges (|E|)':<12} | {'BFS Avg Time (ms)':<18} | {'DFS Avg Time (ms)':<18} | {'Faster Alg'}")
    print("-" * 80)

    results = []

    for size in network_sizes:
        # Generate network with realistic average degree of ~8
        net = generate_random_network(num_users=size, avg_friends=8, seed=42)
        users = net.get_users()
        num_edges = net.num_connections()

        bfs_times = []
        dfs_times = []

        for r in range(runs_per_size):
            start_node = users[(r * 13) % len(users)]

            # Benchmark BFS
            t0 = time.perf_counter()
            _ = net.bfs_traversal(start_node)
            t1 = time.perf_counter()
            bfs_times.append((t1 - t0) * 1000.0)

            # Benchmark DFS
            t0 = time.perf_counter()
            _ = net.dfs_traversal(start_node, iterative=True)
            t1 = time.perf_counter()
            dfs_times.append((t1 - t0) * 1000.0)

        avg_bfs = sum(bfs_times) / len(bfs_times)
        avg_dfs = sum(dfs_times) / len(dfs_times)

        faster = "BFS" if avg_bfs < avg_dfs else "DFS"
        diff_pct = abs(avg_bfs - avg_dfs) / max(avg_bfs, avg_dfs) * 100

        print(f"{size:<12} | {num_edges:<12} | {avg_bfs:<18.4f} | {avg_dfs:<18.4f} | {faster} ({diff_pct:.1f}% faster)")
        results.append({
            "size": size,
            "edges": num_edges,
            "bfs_time": avg_bfs,
            "dfs_time": avg_dfs
        })

    print("-" * 80)
    print("\n[Algorithm Complexity & Empirical Summary]")
    print("1. Theoretical Time Complexity for both BFS & DFS: O(V + E)")
    print("   - In an adjacency list, every vertex is enqueued/pushed once -> O(V)")
    print("   - Every edge is inspected twice (undirected graph) -> O(E)")
    print("2. Empirical Observation:")
    print("   - Both algorithms scale linearly with graph size (V + E).")
    print("   - BFS uses deque.popleft() (FIFO queue), while DFS uses list.pop() (LIFO stack).")
    print("   - BFS finds unweighted shortest path with minimal degrees of separation.")
    print("   - DFS is ideal for connectivity, cycle detection, and finding topological groupings.")
    print("=" * 80 + "\n")

    return results


# =============================================================================
# 5. DEMO APPLICATION
# =============================================================================

def demonstrate_social_network():
    """
    Demonstrates all required features on a representative social graph:
    1. Graph construction (Users & Connections)
    2. BFS Traversal & Shortest Connection Path
    3. DFS Traversal & Connected Components
    4. Mutual Connections
    5. Friend Recommendation Analysis
    """
    print("\n" + "=" * 80)
    print("PROJECT 4: SOCIAL NETWORK CONNECTION AND RECOMMENDATION ANALYSIS")
    print("=" * 80)

    network = SocialNetwork()

    # Create a realistic social network of friends
    friendships = [
        ("Alice", "Bob"),
        ("Alice", "Charlie"),
        ("Alice", "Diana"),
        ("Bob", "Charlie"),
        ("Bob", "Edward"),
        ("Charlie", "Frank"),
        ("Diana", "Frank"),
        ("Diana", "Grace"),
        ("Edward", "Frank"),
        ("Edward", "Henry"),
        ("Frank", "Grace"),
        ("Frank", "Henry"),
        ("Grace", "Ivy"),
        ("Henry", "Jack"),
        # Separate small isolated group (to test disconnected components)
        ("Zara", "Xavier"),
        ("Xavier", "Yusuf")
    ]

    for u1, u2 in friendships:
        network.add_connection(u1, u2)

    print(f"\n[+] Network Initialized Successfully!")
    print(f"    Total Users (Vertices |V|): {network.num_users()}")
    print(f"    Total Friendships (Edges |E|): {network.num_connections()}")
    print(f"    Users: {', '.join(sorted(network.get_users()))}")

    # 1. BFS Traversal
    start_user = "Alice"
    bfs_result = network.bfs_traversal(start_user)
    print(f"\n--- 1. Breadth-First Search (BFS) Exploration from '{start_user}' ---")
    print(f"    BFS Visit Order (Level-by-Level): {' -> '.join(bfs_result)}")

    # Degrees of separation from Alice
    degrees = network.get_connections_by_degrees(start_user, max_degree=3)
    for deg, users in sorted(degrees.items()):
        print(f"    - Degree {deg} Connections ({'Direct' if deg==1 else f'{deg}-hop'}): {', '.join(users)}")

    # 2. DFS Traversal
    dfs_result = network.dfs_traversal(start_user)
    print(f"\n--- 2. Depth-First Search (DFS) Exploration from '{start_user}' ---")
    print(f"    DFS Visit Order (Depth-First): {' -> '.join(dfs_result)}")

    # Connected Components via DFS
    components = network.find_all_components()
    print(f"\n--- 3. Network Clusters / Connected Communities (via DFS) ---")
    print(f"    Total Disconnected Communities: {len(components)}")
    for idx, comp in enumerate(components, 1):
        print(f"    - Community {idx} ({len(comp)} members): {', '.join(sorted(comp))}")

    # 3. Shortest Path using BFS
    src, dst = "Alice", "Jack"
    path, dist = network.find_shortest_path(src, dst)
    print(f"\n--- 4. Shortest Connection Path between '{src}' and '{dst}' (BFS) ---")
    if path:
        print(f"    Shortest Path: {' -> '.join(path)}")
        print(f"    Degrees of Separation: {dist} hop(s)")
    else:
        print(f"    No connection exists between {src} and {dst}.")

    # Shortest path between disconnected users
    src_disc, dst_disc = "Alice", "Zara"
    path_disc, dist_disc = network.find_shortest_path(src_disc, dst_disc)
    print(f"\n--- Shortest Path between Disconnected Users '{src_disc}' and '{dst_disc}' ---")
    if path_disc:
        print(f"    Shortest Path: {' -> '.join(path_disc)}")
    else:
        print(f"    Result: No path exists! They belong to different connected components.")

    # 4. Mutual Connections
    u_a, u_b = "Alice", "Edward"
    mutual = network.get_mutual_connections(u_a, u_b)
    print(f"\n--- 5. Mutual Connections Identification ---")
    print(f"    Direct Friends of {u_a}: {', '.join(sorted(network.get_friends(u_a)))}")
    print(f"    Direct Friends of {u_b}: {', '.join(sorted(network.get_friends(u_b)))}")
    print(f"    Mutual Friends between {u_a} and {u_b}: {', '.join(mutual) if mutual else 'None'}")

    # 5. Friend Recommendations
    target_rec = "Alice"
    recommendations = network.recommend_friends(target_rec, top_k=4)
    print(f"\n--- 6. Friend Recommendation Analysis for '{target_rec}' ('People You May Know') ---")
    for rank, rec in enumerate(recommendations, 1):
        print(f"    Rank #{rank}: {rec['user']}")
        print(f"            Mutual Friends Count : {rec['mutual_count']}")
        print(f"            Mutual Friends List  : {', '.join(rec['mutual_friends'])}")
        print(f"            Jaccard Similarity   : {rec['jaccard_similarity']}")


if __name__ == "__main__":
    # Run core system demonstration
    demonstrate_social_network()

    # Run performance benchmark for varying network sizes
    run_performance_analysis(network_sizes=[100, 500, 1000, 2500, 5000])
