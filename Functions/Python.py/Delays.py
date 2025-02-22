import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Generate synthetic order delivery data
np.random.seed(42)

num_orders = 1000  # Total orders
on_time_deliveries = int(0.70 * num_orders)  # 70% within 0-1 hour
slightly_late_deliveries = int(0.25 * num_orders)  # 25% within 1-2 hours
very_late_deliveries = int(0.05 * num_orders)  # 5% take 3+ hours

# Simulated expected and actual delivery times
expected_delivery = np.random.randint(3, 7, size=num_orders)  # Expected time between 3-7 hours
actual_delivery = np.concatenate([
    expected_delivery[:on_time_deliveries] + np.random.uniform(0, 1, on_time_deliveries),  # 0-1 hr delay
    expected_delivery[on_time_deliveries:on_time_deliveries+slightly_late_deliveries] + np.random.uniform(1, 2, slightly_late_deliveries),  # 1-2 hrs delay
    expected_delivery[on_time_deliveries+slightly_late_deliveries:] + np.random.uniform(3, 5, very_late_deliveries)  # 3+ hrs delay
])

# Create a DataFrame
df = pd.DataFrame({
    "Order_ID": np.arange(1, num_orders+1),
    "Expected_Delivery_Time": expected_delivery,
    "Actual_Delivery_Time": actual_delivery
})
df["Delay"] = df["Actual_Delivery_Time"] - df["Expected_Delivery_Time"]

# Step 2: Estimate Probability Density Function (PDF) for delay times
delay_values = df["Delay"].values
pdf = stats.gaussian_kde(delay_values)

# Generate probabilities for a range of delay values
delay_range = np.linspace(min(delay_values), max(delay_values), 100)
pdf_values = pdf(delay_range)

# Step 3: Normalize Data for Vector Representation
df["Normalized_Expected"] = (df["Expected_Delivery_Time"] - df["Expected_Delivery_Time"].mean()) / df["Expected_Delivery_Time"].std()
df["Normalized_Actual"] = (df["Actual_Delivery_Time"] - df["Actual_Delivery_Time"].mean()) / df["Actual_Delivery_Time"].std()
df["Normalized_Delay"] = (df["Delay"] - df["Delay"].mean()) / df["Delay"].std()

# Create feature vectors
order_vectors = df[["Normalized_Expected", "Normalized_Actual", "Normalized_Delay"]].values

# Compute similarity using Cosine Similarity
similarity_matrix = cosine_similarity(order_vectors)

# Step 4: Find the most similar orders for a random order
random_order_index = np.random.randint(0, num_orders)  # Select a random order
similar_orders = np.argsort(-similarity_matrix[random_order_index])[:5]  # Top 5 similar orders

# Display similar orders
selected_order = df.iloc[random_order_index]
similar_orders_df = df.iloc[similar_orders]

# 🔴 Removed `import ace_tools as tools`
# 🔴 Removed `tools.display_dataframe_to_user()`, replaced with standard Pandas display:
print("\n🔹 Top 5 Similar Orders Based on Delay Patterns:\n", similar_orders_df)

# Step 5: Plot PDF for delays
plt.figure(figsize=(8, 5))
plt.plot(delay_range, pdf_values, label="PDF of Delivery Delays", color="blue")
plt.axvline(x=1, color='red', linestyle="--", label="1-hour Delay Threshold")
plt.axvline(x=2, color='orange', linestyle="--", label="2-hour Delay Threshold")
plt.axvline(x=3, color='green', linestyle="--", label="3-hour Delay Threshold")
plt.xlabel("Hours of Delay")
plt.ylabel("Probability Density")
plt.title("Probability Density Function of Order Delivery Delays")
plt.legend()
plt.show()

# Step 6: Plot Top 5 Similar Orders' Similarity Scores
plt.figure(figsize=(8, 5))
plt.bar(["Order "+str(i) for i in range(1, 6)], similarity_matrix[random_order_index][similar_orders], color="skyblue")
plt.xlabel("Similar Order Index")
plt.ylabel("Similarity Score")
plt.title("Top 5 Similar Orders Based on Delay Patterns")
plt.show()
