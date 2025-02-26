# Given data
total_students = 100  # Total number of students
students_scoring_80_or_less = 84  # Students who scored ≤ 80

# Compute CMF
cmf_80 = students_scoring_80_or_less / total_students

# Print result
print(f"Probability of scoring ≤ 80 marks: {cmf_80:.2f} ({cmf_80 * 100:.2f}%)")