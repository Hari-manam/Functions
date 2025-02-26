import numpy as np
from scipy import stats

# Cookie data
data = [2, 3, 4, 5, 3, 6, 2, 4, 5, 3]

# Point Estimation
average = np.mean(data)
print(f"Average cookies eaten: {average:.1f}")

# Confidence Interval (95%)
std_dev = np.std(data, ddof=1)  # Sample standard deviation
margin = stats.t.ppf(0.975, len(data)-1) * (std_dev / np.sqrt(len(data)))
conf_interval = (average - margin, average + margin)
print(f"95% Confidence Interval: [{conf_interval[0]:.1f}, {conf_interval[1]:.1f}]")

# Hypothesis Testing (vs old average of 3)
t_stat, p_value = stats.ttest_1samp(data, 3)
print(f"Hypothesis Test p-value: {p_value:.3f} (if < 0.05, new recipe is better)")

# Sensitivity (for 5+ cookies)
lovers = sum(1 for x in data if x >= 5)  # True lovers
guessed_lovers = lovers  # We guess all correctly
sensitivity = guessed_lovers / lovers
print(f"Sensitivity: {sensitivity:.2f}")

# Entropy (simplified binary: <4 vs 4+)
probs = [sum(1 for x in data if x < 4) / len(data), sum(1 for x in data if x >= 4) / len(data)]
entropy = -sum(p * np.log2(p) for p in probs if p > 0)
print(f"Entropy: {entropy:.2f} bits")

# Information Gain (rough estimate, comparing entropy before/after)
prior_entropy = 1  # Assuming max uncertainty (50-50) before data
info_gain = prior_entropy - entropy
print(f"Information Gain: {info_gain:.2f} bits")