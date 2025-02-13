# heights

from scipy.stats import norm

print(norm.cdf(6, 5.5, 0.25) - norm.cdf(5, 5.5, 0.25))

# 5 matches team scores

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

scores = [140, 120, 130, 145, 122]  # Match scores
mu, sigma = np.mean(scores), np.std(scores)  # Mean & Std Dev

x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)  # X-axis values
plt.plot(x, norm.pdf(x, mu, sigma))  # Plot Normal Distribution
plt.axvline(mu, color="red", linestyle="dashed")  # Mark Mean
plt.title("Normal Distribution of Match Scores")
plt.show()