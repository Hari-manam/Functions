# Can Penguins fly?
import numpy as np

question = "Can penguins fly?"
answer = np.random.binomial(0.1, 1)  # 10% chance of True, 90% False

print(question, "→", "True" if answer else "False")

# pass or fail in exam

import numpy as np

# Simulate pass/fail for 10 students (70% pass, 30% fail)
results = np.random.choice([1, 0], size=10, p=[0.7, 0.3])

print(f"Results: {results}")
print(f"Passed: {np.sum(results)}, Failed: {len(results) - np.sum(results)}")

# are oceans are salty?

import numpy as np

# Simulate responses from 10 people (99% say "Yes", 1% say "No")
responses = np.random.choice(["Yes", "No"], size=10, p=[0.99, 0.01])

print(f"Responses: {responses}")
print(f"Yes: {np.sum(responses == 'Yes')}, No: {np.sum(responses == 'No')}")

# The outcomes of either buying are not buying product in grocessary store

import numpy as np

# Simulate one customer's decision (80% buy, 20% not buy)
customer_decision = np.random.choice(["Buy", "Not Buy"], p=[0.8, 0.2])

print(f"Customer Decision: {customer_decision}")

# What are the chances of that application will pick up for a job?

import numpy as np

# Simulate job application result (30% chance of selection, 70% rejection)
job_application = np.random.choice(["Selected", "Rejected"], p=[0.3, 0.7])

print(f"Job Application Result: {job_application}")





