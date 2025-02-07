# Re-import necessary libraries after execution state reset
import numpy as np
import pandas as pd
from scipy import stats

# Sample data: Inventory levels and corresponding prices
inventory = np.array([100, 120, 150, 180, 200, 250, 300, 350, 400, 450])
price = np.array([50, 48, 45, 43, 40, 38, 35, 33, 30, 28])  # Prices decrease as inventory increases

# Calculate correlation
correlation = np.corrcoef(inventory, price)[0, 1]

# Calculate statistics
mode_result = stats.mode(price)
mode_value = mode_result.mode[0] if isinstance(mode_result.mode, np.ndarray) and mode_result.mode.size > 0 else mode_result.mode

stats_data = {
    "Mean": np.mean(price),
    "Median": np.median(price),
    "Mode": mode_value,
    "Standard Deviation": np.std(price, ddof=1),
    "Variance": np.var(price, ddof=1)
}

# Display results
print(correlation, stats_data)

# correlation between speed and acceleration and find the mean median mode, standard deviation, variance

# Re-import necessary libraries after execution state reset
import numpy as np
from scipy import stats

# Sample data: Speed (km/h) and Acceleration (m/s²)
speed = np.array([20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
acceleration = np.array([2.5, 2.3, 2.1, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7])  # Acceleration decreases as speed increases

# Calculate correlation
correlation = np.corrcoef(speed, acceleration)[0, 1]

# Calculate statistics for acceleration
stats_data = {
    "Mean": np.mean(acceleration),
    "Median": np.median(acceleration),
    "Mode": mode_value,
    "Standard Deviation": np.std(acceleration, ddof=1),
    "Variance": np.var(acceleration, ddof=1)
}

# Display results