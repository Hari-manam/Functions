# Given data
total_population = 1000  # Total number of people
medicine_x_users = 300   # People using Medicine X
medicine_y_users = 400   # People using Medicine Y

# Assuming no one takes both medicines
people_not_using_any = total_population - (medicine_x_users + medicine_y_users)

# Compute PMF
pmf_no_medicine = people_not_using_any / total_population

# Print results
print(f"Total Population: {total_population}")
print(f"People who did not use any medicine: {people_not_using_any}")
print(f"PMF for not using either medicine: {pmf_no_medicine:.2f} ({pmf_no_medicine * 100:.2f}%)")