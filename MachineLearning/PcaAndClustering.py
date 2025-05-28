import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage

# Step 1: Load and clean data
df = pd.read_csv(r"C:\Users\nanim\OneDrive\Desktop\Datasets\healthcare-dataset-stroke-data.csv")
df = df.dropna(subset=['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi'])

# Step 2: Select and scale features
features = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: PCA transformation
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("🔹 Explained Variance Ratio (PCA):", pca.explained_variance_ratio_)

# Step 4: Plot PCA result
plt.figure(figsize=(6, 5))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1])
plt.title("PCA Projection")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.grid(True)
plt.show()

# Step 5: Hierarchical Clustering Dendrogram
linked = linkage(X_pca, method='ward')  # linkage on PCA output

plt.figure(figsize=(12, 6))
dendrogram(linked, truncate_mode='lastp', p=30, leaf_rotation=90., leaf_font_size=10., show_contracted=True)
plt.title("Hierarchical Clustering Dendrogram (on PCA output)")
plt.xlabel("Data Points (grouped)")
plt.ylabel("Distance")
plt.grid(True)
plt.show()

# Step 6: Agglomerative Clustering (3 clusters for consistency)
hier_model = AgglomerativeClustering(n_clusters=3)
hier_labels = hier_model.fit_predict(X_pca)

plt.figure(figsize=(6, 5))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=hier_labels, palette='Set2')
plt.title("Hierarchical Clustering on PCA Data")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

# Step 7: K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans_labels = kmeans.fit_predict(X_pca)
centroids = kmeans.cluster_centers_

# Plot K-Means Results
plt.figure(figsize=(6, 5))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=kmeans_labels, palette='Set1')
plt.scatter(centroids[:, 0], centroids[:, 1], s=200, c='black', marker='X', label='Centroids')
plt.title("K-Means Clustering on PCA Data")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

# Step 8: Print K-Means outputs
print("🔹 K-Means Cluster Assignments:")
print(kmeans_labels)

print("\n🔹 Final K-Means Centroids (PCA space):")
print(centroids)
