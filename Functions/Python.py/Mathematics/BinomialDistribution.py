# Compute probability of getting exactly 3 job offers

import numpy as np
from scipy.stats import binom

n, p = 10, 0.3  # 10 job applications, 30% selection chance

# Simulate the number of job offers
job_offers = np.random.binomial(n, p)

# Compute probability of getting exactly 3 job offers
prob_3_jobs = binom.pmf(3, n, p) * 100  # Convert to percentage

print(f"Number of job offers received: {job_offers} out of {n}")
print(f"Probability of getting exactly 3 job offers: {prob_3_jobs:.2f}%")

# Compute probability of getting exactly 6 job offers

import numpy as np
from scipy.stats import binom

n, p = 10, 0.3  # 10 job applications, 30% selection chance

# Simulate the number of job offers
job_offers = np.random.binomial(n, p)

# Compute probability of getting exactly 3 job offers
prob_6_jobs = binom.pmf(6, n, p) * 100  # Convert to percentage

print(f"Number of job offers received: {job_offers} out of {n}")
print(f"Probability of getting exactly 6 job offers: {prob_6_jobs:.2f}%")

# Public opinion polls 

import numpy as np
from scipy.stats import binom

n, p = 1000, 0.6  # 1000 people surveyed, 60% probability of saying "Yes"

# Simulate the number of "Yes" responses
yes_responses = np.random.binomial(n, p)

# Compute probabilities for exactly 200, 300, 400, and 600 "Yes" responses
probabilities = {k: binom.pmf(k, n, p) * 100 for k in [200, 300, 400, 600]}

print(f"Number of 'Yes' responses: {yes_responses} out of {n}")
for k, prob in probabilities.items():
    print(f"Probability of exactly {k} people saying 'Yes': {prob:.4f}%")

