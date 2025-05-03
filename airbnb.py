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

# --- Step 3: Handle Missing Values (NaNs or Blanks) ---
print("\n--- Step 3: Handle Missing Values ---")

# Identify Missing Data: Get the count of missing values per column
print("\nMissing values per column:")
missing_counts = df.isnull().sum()
print(missing_counts)

# Decide on a Strategy (Implementing examples based on your plan):

# NAME: Fill with 'Unknown Listing'
if 'NAME' in df.columns:
    if missing_counts['NAME'] > 0:
        df['NAME'].fillna('Unknown Listing', inplace=True)
        print(f"\nFilled {missing_counts['NAME']} missing values in 'NAME' with 'Unknown Listing'.")
    else:
         print("\nNo missing values in 'NAME'.")
else:
    print("\nWarning: 'NAME' column not found.")

# host id:dropping rows if problematic.
# We'll check if host id is numeric first, as missing numeric values are NaN
if 'host id' in df.columns:
     # Ensure host id is treated correctly - check if it's numeric or object
     if pd.api.types.is_numeric_dtype(df['host id']):
        if missing_counts['host id'] > 0:
            initial_rows = df.shape[0]
            df.dropna(subset=['host id'], inplace=True)
            rows_after_dropping = df.shape[0]
            dropped_rows = initial_rows - rows_after_dropping
            print(f"\nDropped {dropped_rows} rows due to missing 'host id'. Remaining rows: {rows_after_dropping}.")
        else:
             print("\nNo missing values in 'host id'.")
     else: # If host id is object/string type, NaNs might be represented differently, or just check isnull()
           if missing_counts['host id'] > 0:
                initial_rows = df.shape[0]
                df.dropna(subset=['host id'], inplace=True)
                rows_after_dropping = df.shape[0]
                dropped_rows = initial_rows - rows_after_dropping
                print(f"\nDropped {dropped_rows} rows due to missing 'host id' (object type). Remaining rows: {rows_after_dropping}.")
           else:
                print("\nNo missing values in 'host id' (object type).")
else:
    print("\nWarning: 'host id' column not found.")


# host_name: Fill with 'Unknown Host' (or consider dropping the column later if not needed)
if 'host name' in df.columns:
     if missing_counts['host name'] > 0:
        df['host name'].fillna('Unknown Host', inplace=True)
        print(f"\nFilled {missing_counts['host name']} missing values in 'host name' with 'Unknown Host'.")
     else:
          print("\nNo missing values in 'host name'.")
else:
    print("\nWarning: 'host name' column not found.")


# host_identity_verified: Fill missing with 'Unknown'
if 'host_identity_verified' in df.columns:
     if missing_counts['host_identity_verified'] > 0:
        df['host_identity_verified'].fillna('Unknown', inplace=True)
        print(f"\nFilled {missing_counts['host_identity_verified']} missing values in 'host_identity_verified' with 'Unknown'.")
     else:
         print("\nNo missing values in 'host_identity_verified'.")
else:
    print("\nWarning: 'host_identity_verified' column not found.")


# neighbourhood_group, neighbourhood: Fill with 'Unknown' or 'Not Specified'
location_cols = ['neighbourhood group', 'neighbourhood']
for col in location_cols:
     if col in df.columns:
         if missing_counts[col] > 0:
            df[col] = df[col].fillna('Unknown', inplace=True)
            print(f"\nFilled {missing_counts[col]} missing values in '{col}' with 'Unknown'.")
         else:
             print(f"\nNo missing values in '{col}'.")
     else:
         print(f"\nWarning: '{col}' column not found.")


# lat, long: Drop rows if missing (as suggested, crucial for mapping)
lat_long_cols = ['lat', 'long']
initial_rows = df.shape[0] # Get current row count before dropping

for col in lat_long_cols:
     if col in df.columns:
        if missing_counts[col] > 0:
            # Drop rows where either lat or long is missing
            df.dropna(subset=[col], inplace=True)
            print(f"\nDropped rows due to missing values in '{col}'.") # Message updated below after loop
        else:
             print(f"\nNo missing values in '{col}'.")
     else:
         print(f"\nWarning: '{col}' column not found.")

# Calculate and print the total number of rows dropped for lat/long
rows_after_dropping = df.shape[0]
dropped_rows_lat_long = initial_rows - rows_after_dropping
if dropped_rows_lat_long > 0:
     print(f"\nTotal rows dropped due to missing 'lat' or 'long': {dropped_rows_lat_long}. Remaining rows: {rows_after_dropping}.")


# country: Fill missing with 'Unknown'
if 'country' in df.columns:
     if missing_counts['country'] > 0:
        df['country'].fillna('Unknown', inplace=True)
        print(f"\nFilled {missing_counts['country']} missing values in 'country' with 'Unknown'.")
     else:
         print("\nNo missing values in 'country'.")
else:
    print("\nWarning: 'country' column not found.")


# Re-check missing values after handling
print("\nMissing values after handling:")
print(df.isnull().sum())