import numpy as np;
import pandas as pd;



# Replace 'path/to/your/downloaded/file.csv' with the actual path to your file
# Make sure to use forward slashes / or double backslashes \\ in Windows paths
file_path = "C:\\Users\\HP\\Desktop\\gitprojects\\Airbnb\\Airbnb_Open_Data.csv" # Example path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# --- Step 1: Load and Initial Inspection ---
print("\n--- Step 1: Initial Inspection ---")

# Understand the Structure: Check the dimensions
print("\nShape of the dataset (rows, columns):", df.shape)

# Examine the first few rows
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Examine the last few rows (optional, but good practice)
# print("\nLast 5 rows of the dataset:")
# print(df.tail())

# Get a summary of data types and non-null counts
print("\nInfo about data types and non-null counts:")
df.info()

# Get descriptive statistics for numerical columns
# Includes lat and long if they are numeric type
print("\nDescriptive statistics for numerical columns:")
print(df.describe())

# Get counts of unique values for categorical columns
print("\nUnique value counts for key categorical columns:")

categorical_cols = ['neighbourhood group', 'neighbourhood', 'country', 'host_identity_verified']

for col in categorical_cols:
    if col in df.columns:
        print(f"\nCounts for '{col}':")
        # .value_counts() excludes NaN by default, add dropna=False to include NaNs if needed
        print(df[col].value_counts(dropna=False))
    else:
        print(f"\nWarning: Column '{col}' not found in the dataset.")

# --- Step 2: Handle Duplicate Listings ---
print("\n--- Step 2: Handle Duplicate Listings ---")

# Identify Duplicates: Check for duplicate rows based on the listing 'id'
# .duplicated() returns a boolean Series, sum() counts the True values
if 'id' in df.columns:
    num_duplicates = df.duplicated(subset=['id']).sum()
    print(f"\nNumber of duplicate listings based on 'id': {num_duplicates}")

    # Remove Duplicates: If duplicates are found, remove them
    if num_duplicates > 0:
        initial_rows = df.shape[0]
        # keep='first' keeps the first occurrence, inplace=True modifies the DataFrame directly
        df.drop_duplicates(subset=['id'], keep='first', inplace=True)
        rows_after_dropping = df.shape[0]
        print(f"Removed {num_duplicates} duplicate rows. Remaining rows: {rows_after_dropping}")
    else:
        print("No duplicate listings found based on 'id'.")
else:
    print("\nWarning: 'id' column not found. Cannot check for duplicate listings based on id.")

