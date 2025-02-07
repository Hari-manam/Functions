# Election voters poll simulation
import random

# Simulating a population of 1 million voters with random choices for 3 candidates
population_size = 1_000_000
voters = ["Candidate A", "Candidate B", "Candidate C"]
population_votes = [random.choice(voters) for _ in range(population_size)]

# Selecting a random sample of 1000 voters
sample_size = 1000
sample_votes = random.sample(population_votes, sample_size)

# Counting votes in the sample
vote_counts = {candidate: sample_votes.count(candidate) for candidate in voters}

# Displaying election poll results from the sample
print(vote_counts)

#product quality testing

import random

# Simulating 1000 phones where each phone is either "Defective" or "Good"
population_size = 1000
phones = ["Good"] * 950 + ["Defective"] * 50  # 95% Good, 5% Defective

# Selecting a random sample of 100 phones for testing
sample_size = 100
sample_phones = random.sample(phones, sample_size)

# Counting defective and good phones in the sample
quality_check = {"Good": sample_phones.count("Good"), "Defective": sample_phones.count("Defective")}

# Displaying product quality test results
print(quality_check)

#Medical Research

import random

# Simulating a population of 10,000 patients for a medical drug trial
population_size = 10_000
patients = ["Receives Drug"] * 5000 + ["Receives Placebo"] * 5000  # 50% get the drug, 50% get a placebo

# Selecting a random sample of 500 patients for the study
sample_size = 500
sample_patients = random.sample(patients, sample_size)

# Counting how many received the drug vs placebo in the sample
trial_results = {
    "Receives Drug": sample_patients.count("Receives Drug"),
    "Receives Placebo": sample_patients.count("Receives Placebo"),
}

# Displaying medical trial results
print(trial_results)
