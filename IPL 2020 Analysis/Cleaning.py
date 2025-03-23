import pandas as pd

# 1. Load the CSV file (make sure 'ipl_records_combined.csv' is in your current directory)
df = pd.read_csv("ipl_records_combined.csv")

# 2. Inspect the data
print("Initial columns:", df.columns.tolist())
print("Preview of the data:")
print(df.head())

# 3. Clean Column Names: Strip whitespace, convert to lowercase, replace spaces with underscores
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# 4. Drop any columns that are completely empty (if any)
df = df.dropna(axis=1, how="all")

# 5. Fill missing values with an empty string (or a placeholder of your choice)
df = df.fillna("")

# 6. Remove duplicate rows
df = df.drop_duplicates()

# 7. Reorder Columns: If "record_type" is present, move it to the first column
if "record_type" in df.columns:
    cols = df.columns.tolist()
    cols.remove("record_type")
    new_order = ["record_type"] + cols
    df = df[new_order]

# 8. (Optional) Sort the DataFrame by record_type for better organization
if "record_type" in df.columns:
    df = df.sort_values("record_type")

# 9. Save the cleaned and organized DataFrame to a new CSV file in the current directory
output_filename = "ipl_records_combined_cleaned.csv"
df.to_csv(output_filename, index=False)
print(f"\nCleaned CSV saved to '{output_filename}'.")

# 10. Final inspection
print("Final columns:", df.columns.tolist())
print("Final preview:")
print(df.head())
