import csv
import pandas as pd

# Load the table data from 'table.csv'
inittable = []
with open('table.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        inittable.append(row)

# Convert the table to a pandas DataFrame for easier manipulation
df = pd.DataFrame(inittable)

# Define your functional dependencies. This should be in the format:
# 'X' -> 'Y' means that X determines Y
functional_dependencies = {
    'A': 'B',
    'C': 'D',
    # Add your functional dependencies here
}

# Initialize a dictionary to store multivalued dependencies
multivalued_dependencies = {}

# Step 1: Check for multivalued dependencies
for lhs, rhs in functional_dependencies.items():
    for index, row in df.iterrows():
        # Split the attributes on both sides of the functional dependency
        lhs_values = set(row[lhs].split(','))
        rhs_values = set(row[rhs].split(','))
        
        # Check if any value in the LHS has more than one corresponding value in the tuples
        for value in lhs_values:
            if sum(1 for r in df[rhs] if value in r.split(',')) > 1:
                multivalued_dependencies[lhs] = rhs

# Step 2: Normalize the table to 4NF
# Assuming that multivalued dependencies are marked correctly, we can proceed to normalization.

# Create a new table for each multivalued dependency and remove duplicates
normalized_tables = []
for lhs, rhs in multivalued_dependencies.items():
    new_table = df[[lhs, rhs]].drop_duplicates()
    normalized_tables.append(new_table)

# Display the normalized tables
for idx, table in enumerate(normalized_tables):
    table.to_csv(f'normalized_table_{idx}.csv', index=False)
