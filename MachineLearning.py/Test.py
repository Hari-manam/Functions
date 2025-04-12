import numpy as np
import pandas as pd
from itertools import combinations
from collections import defaultdict

# Step 1: Define 6 points in 2D space
points = {
    'a': np.array([0, 0]),
    'b': np.array([8, 0]),
    'c': np.array([16, 0]),
    'd': np.array([0, 6]),
    'e': np.array([8, 6]),
    'f': np.array([16, 6])
}

point_names = list(points.keys())
coords = np.array([points[p] for p in point_names])

# Step 2: Euclidean distance function
def euclidean(p1, p2):
    return np.linalg.norm(p1 - p2)

# Step 3: Custom 3-means clustering with tie-breaking
def kmeans(points_dict, initial_centroids, max_iter=10):
    names = list(points_dict.keys())
    coords = np.array([points_dict[n] for n in names])
    centroids = [points_dict[c] for c in initial_centroids]
    cluster_map = {}

    for _ in range(max_iter):
        new_cluster_map = defaultdict(list)

        for i, p in enumerate(coords):
            distances = [euclidean(p, c) for c in centroids]
            min_dist = min(distances)
            candidates = [i for i, d in enumerate(distances) if d == min_dist]

            if len(candidates) > 1:
                chosen = min(candidates, key=lambda idx: (centroids[idx][0], centroids[idx][1]))
            else:
                chosen = candidates[0]

            new_cluster_map[chosen].append(i)

        # Recompute centroids
        new_centroids = []
        for idx in sorted(new_cluster_map.keys()):
            cluster_points = [coords[i] for i in new_cluster_map[idx]]
            new_centroids.append(np.mean(cluster_points, axis=0))

        if all(np.allclose(centroids[i], new_centroids[i]) for i in range(len(centroids))):
            break
        centroids = new_centroids
        cluster_map = new_cluster_map

    final_partition = []
    for idx in sorted(cluster_map.keys()):
        cluster_names = [names[i] for i in cluster_map[idx]]
        final_partition.append(tuple(sorted(cluster_names)))

    return tuple(sorted(final_partition))

# Step 4: Run all starting configurations (20 total)
starting_configs = list(combinations(points.keys(), 3))
partition_counts = defaultdict(int)
config_to_partition = {}

for config in starting_configs:
    result = kmeans(points, config)
    partition_counts[result] += 1
    config_to_partition[config] = result

# Step 5: Create and print a summary DataFrame
results = []
seen_partitions = set()

for config, partition in config_to_partition.items():
    if partition not in seen_partitions:
        results.append({
            "Starting_Config": str(config),
            "Stable_3-Partition": str(partition),
            "Count": partition_counts[partition]
        })
        seen_partitions.add(partition)

results_df = pd.DataFrame(results)

# Step 6: Print results and save to CSV
print("\nStable 3-Means Partitions Summary:\n")
print(results_df.to_string(index=False))


