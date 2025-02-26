from scipy.stats import norm

# Given values
mean_bp = 120  # Mean blood pressure
std_dev = 15   # Standard deviation
x1, x2 = 100, 140  # Blood pressure range

# Compute probability using CDF
probability = norm.cdf(x2, mean_bp, std_dev) - norm.cdf(x1, mean_bp, std_dev)

print(f"Probability of blood pressure between 100 and 140: {probability:.4f} ({probability * 100:.2f}%)")