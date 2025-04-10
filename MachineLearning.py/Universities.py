import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

# Load dataset
file_path = r'N:\Universities.csv'  # Change this to your actual path if needed
df = pd.read_csv(file_path)

# Step 1: Remove records with any missing values (for clustering)
continuous_cols = df.columns[3:20]  # 17 continuous attributes
complete_df = df.dropna(subset=continuous_cols).copy()

# Step 2: Normalize and perform hierarchical clustering
X = complete_df[continuous_cols]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
linked = linkage(X_scaled, method='complete', metric='euclidean')

# Step 3: Dendrogram
plt.figure(figsize=(12, 6))
dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=False)
plt.title("Dendrogram for Hierarchical Clustering")
plt.xlabel("Colleges")
plt.ylabel("Euclidean Distance")
plt.axhline(y=20, color='r', linestyle='--')  # Optional cutoff guide
plt.show()

# Step 4: Form clusters
num_clusters = 4  # You can adjust based on dendrogram
cluster_labels = fcluster(linked, num_clusters, criterion='maxclust')
complete_df['Cluster'] = cluster_labels

# Step 5: Summary statistics per cluster
cluster_summary = complete_df.groupby('Cluster')[continuous_cols].mean()
print("\nCluster Summary Statistics:\n", cluster_summary)

# Step 6: Link clusters to categorical variables
public_private_relation = pd.crosstab(complete_df['Cluster'], complete_df['Public (1)/ Private (2)'])
print("\nPublic/Private Distribution by Cluster:\n", public_private_relation)

state_relation = complete_df.groupby('Cluster')['State'].value_counts().groupby(level=0).nlargest(5)
print("\nTop 5 States per Cluster:\n", state_relation)

# Step 7: Impute missing values for Tufts University
tufts = df[df['College Name'].str.contains("Tufts", case=False, na=False)].copy()
if not tufts.empty:
    tufts_index = tufts.index[0]
    tufts_known = tufts[continuous_cols].iloc[0]
    known_features = tufts_known.dropna().index.tolist()

    cluster_centroids = complete_df.groupby('Cluster')[continuous_cols].mean()
    tufts_scaled = scaler.transform(tufts[continuous_cols])[0]
    tufts_scaled_known = [tufts_scaled[X.columns.get_loc(col)] for col in known_features]
    centroids_scaled = scaler.transform(cluster_centroids)[..., [X.columns.get_loc(col) for col in known_features]]
    distances = cdist([tufts_scaled_known], centroids_scaled, metric='euclidean')
    closest_cluster = np.argmin(distances) + 1

    # Impute missing values
    imputed_values = cluster_centroids.loc[closest_cluster]
    tufts_imputed = tufts_known.copy()
    for col in tufts_known.index:
        if pd.isna(tufts_known[col]):
            tufts_imputed[col] = imputed_values[col]

    tufts_filled = tufts.copy()
    for col in continuous_cols:
        tufts_filled.loc[tufts_index, col] = tufts_imputed[col]

    print(f"\nTufts was assigned to Cluster {closest_cluster}")
    print("\nImputed Tufts University Record:\n", tufts_filled[continuous_cols])
else:
    print("Tufts University not found in the dataset.")

# Optional: Save results to CSV
# cluster_summary.to_csv("cluster_summary.csv")
# public_private_relation.to_csv("public_private_distribution.csv")
# state_relation.to_csv("state_distribution.csv")
# tufts_filled.to_csv("tufts_imputed.csv", index=False)
