import numpy as np
import matplotlib.pyplot as plt

# Define dataset
study_hours = np.array([6, 3, 1, 5, 2])  # X-axis
attendance = np.array([1, 1, 0, 0, 0])  # Y-axis (1 = Yes, 0 = No)
labels = np.array(["Pass", "Pass", "Fail", "Pass", "Fail"])  # Outcomes

# Create a scatter plot
plt.figure(figsize=(8,6))

# Plot each student as a point
for i in range(len(study_hours)):
    color = "green" if labels[i] == "Pass" else "red"
    plt.scatter(study_hours[i], attendance[i], color=color, s=200, edgecolors="black", label=labels[i] if labels[i] not in plt.gca().get_legend_handles_labels()[1] else "")

# Draw the first decision boundary: Study Hours = 3
plt.axvline(x=3, color="blue", linestyle="--", linewidth=2, label="Study Hours = 3 (Decision Boundary)")

# Annotate the decision rule
plt.text(3.2, 0.5, "Study Hours > 3?", color="blue", fontsize=12, rotation=90, verticalalignment='center')

# Add labels
plt.xlabel("Study Hours")
plt.ylabel("Attendance (1 = Yes, 0 = No)")
plt.title("Decision Tree Split for Pass/Fail Prediction")

# Legend
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
