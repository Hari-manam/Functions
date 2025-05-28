import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = r'N:\Universities.csv'
df = pd.read_csv(file_path)

# (a) Remove records with any missing values (for clustering)
continuous_cols = df.columns[3:20]
complete_df = df.dropna(subset=continuous_cols).copy()

# (b) Normalize and perform hierarchical clustering
X = complete_df[continuous_cols]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
linked = linkage(X_scaled, method='complete', metric='euclidean')

# Dendrogram visualization
plt.figure(figsize=(12, 6))
dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=False)
plt.title("Dendrogram for Hierarchical Clustering")
plt.xlabel("Colleges")
plt.ylabel("Euclidean Distance")
plt.axhline(y=20, color='r', linestyle='--')
plt.show()

# Define clusters (based on dendrogram inspection)
num_clusters = 4
complete_df['Cluster'] = fcluster(linked, num_clusters, criterion='maxclust')

# (c) Summary statistics per cluster visualization
plt.figure(figsize=(14, 8))
sns.heatmap(complete_df.groupby('Cluster')[continuous_cols].mean().T, annot=True, cmap='coolwarm')
plt.title("Summary Statistics per Cluster")
plt.show()

# (d) Visualizing categorical distribution (Public/Private)
plt.figure(figsize=(12, 6))
sns.countplot(data=complete_df, x='Cluster', hue='Public (1)/ Private (2)')
plt.title("Public/Private Distribution by Cluster")
plt.xlabel("Cluster")
plt.ylabel("Count")
plt.legend(title='Public(1)/Private(2)')
plt.show()

# State distribution per cluster visualization
state_distribution = complete_df.groupby('Cluster')['State'].value_counts().groupby(level=0).nlargest(5).unstack(level=0)
state_distribution.plot(kind='bar', figsize=(15, 8))
plt.title("Top 5 States per Cluster")
plt.xlabel("State")
plt.ylabel("Count")
plt.legend(title="Cluster")
plt.show()

# (f) Imputation for Tufts University
tufts = df[df['College Name'].str.contains("Tufts", case=False, na=False)].copy()
if not tufts.empty:
    tufts_index = tufts.index[0]
    tufts_known = tufts[continuous_cols].iloc[0]
    known_features = tufts_known.dropna().index.tolist()

    cluster_centroids = complete_df.groupby('Cluster')[continuous_cols].mean()

    tufts_scaled_full = scaler.transform([tufts_known.fillna(cluster_centroids.mean())])[0]
    tufts_scaled_known = np.array([tufts_scaled_full[X.columns.get_loc(col)] for col in known_features])

    centroids_scaled = scaler.transform(cluster_centroids)[:, [X.columns.get_loc(col) for col in known_features]]

    distances = cdist([tufts_scaled_known], centroids_scaled, metric='euclidean').flatten()
    closest_cluster = np.argmin(distances) + 1

    plt.figure(figsize=(8, 5))
    sns.barplot(x=[f'Cluster {i+1}' for i in range(len(distances))], y=distances)
    plt.title("Euclidean Distance from Tufts to Clusters")
    plt.ylabel("Distance")
    plt.xlabel("Clusters")
    plt.show()

    imputed_values = cluster_centroids.loc[closest_cluster]
    tufts_imputed = tufts_known.copy()
    for col in continuous_cols:
        if pd.isna(tufts_known[col]):
            tufts_imputed[col] = imputed_values[col]

    tufts.loc[tufts_index, continuous_cols] = tufts_imputed

    print(f"\nTufts University is closest to Cluster {closest_cluster}.")
    print("\nImputed Tufts University Record:\n")
    print(tufts[['College Name'] + list(continuous_cols)].iloc[0])
else:
    print("Tufts University not found in the dataset.")
