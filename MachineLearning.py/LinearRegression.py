import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# --- Step 1: Generate Synthetic Dataset ---
np.random.seed(42)  # For reproducibility
n_samples = 100

# Features
square_footage = np.random.uniform(500, 3000, n_samples)  # Continuous: 500-3000 sq ft
bedrooms = np.random.uniform(1.0, 5.0, n_samples)        # Continuous: 1.0-5.0 bedrooms

# Target (House Price in $10,000s) with some noise
house_price = 0.01 * square_footage + 2 * bedrooms + np.random.normal(0, 1, n_samples)  # Linear relationship + noise

# Combine into a DataFrame
import pandas as pd
data = pd.DataFrame({
    'Square_Footage': square_footage,
    'Bedrooms': bedrooms,
    'House_Price': house_price
})

# --- Step 2: Prepare Data ---
X = data[['Square_Footage', 'Bedrooms']]  # Features
y = data['House_Price']                   # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 3: Train Linear Regression Model ---
model = LinearRegression()
model.fit(X_train, y_train)

# --- Step 4: Make Predictions and Evaluate ---
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"R² Score (Accuracy): {r2:.2f}")
print(f"Coefficients: Square_Footage = {model.coef_[0]:.4f}, Bedrooms = {model.coef_[1]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")

# --- Step 5: Visualization ---
# Scatter plot of actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)  # Ideal line
plt.xlabel("Actual House Price ($10,000s)")
plt.ylabel("Predicted House Price ($10,000s)")
plt.title("Linear Regression: Actual vs Predicted House Prices")
plt.show()

# Optional: 3D visualization of the plane (Square_Footage vs Bedrooms vs Price)
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['Square_Footage'], data['Bedrooms'], data['House_Price'], c='b', marker='o')
x_range = np.linspace(min(square_footage), max(square_footage), 10)
y_range = np.linspace(min(bedrooms), max(bedrooms), 10)
x_grid, y_grid = np.meshgrid(x_range, y_range)
z_grid = model.coef_[0] * x_grid + model.coef_[1] * y_grid + model.intercept_
ax.plot_surface(x_grid, y_grid, z_grid, color='r', alpha=0.5)
ax.set_xlabel("Square Footage (sq ft)")
ax.set_ylabel("Bedrooms")
ax.set_zlabel("House Price ($10,000s)")
ax.set_title("Linear Regression: 3D Fit")
plt.show()

# --- Step 6: Example Prediction ---
new_data = pd.DataFrame({
    'Square_Footage': [2000],
    'Bedrooms': [3.5]
})
predicted_price = model.predict(new_data)
print(f"Predicted House Price for 2000 sq ft and 3.5 bedrooms: ${predicted_price[0] * 10000:.2f}")