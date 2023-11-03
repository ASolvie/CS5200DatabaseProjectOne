import helper
import csv
import sqlite3

#note: helper not actually used here, didn't see the need to.

def reorganize_for_1NF(tablename, db_filename):
    # rows array represents initial table
    rows = []
    # bad_rows stores indexes of rows in rows array with non_atomic values
    bad_loc = []
    # new_table is for building new, 1NF table
    new_table = []
    # split_vals is for storing the multivalued att's split into str lists. somewhat 2d array
    split_vals = []

    bad_rows = []

    # open csv file in text mode, read into list of lists (rows array)
    with open(tablename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            rows.append(row)
    
    # add variable name / header row to new table
    new_table.append(rows[0])
    
    #check for non_atomics in initial table
    for i in range(1, len(rows)):
        non_atom_flag = False
        for j in range(len(rows[i])):
            #check occurs here
            if rows[i][j].startswith("{") and rows[i][j].endswith("}"):
                non_atom_flag = True
                # store in bad_rows
                bad_rows.append(rows[i])
                # store split multival in split_vals
                split_vals.append(rows[i][j].split(","))
                # store row location of non_atomic value in bad_rows
                bad_loc.append(j)
        if not non_atom_flag:
            # append all rows from init table with no non_atomic values
            new_table.append(rows[i])
    
    # Generate new rows using bad_rows, split_vals, and bad_loc
    for i in range(len(bad_loc)):
        for j in range(len(split_vals[i])):
            # Clone the original row and modify the non-atomic value
            new_row = bad_rows[i][:]  # Clone the original row
            new_row[bad_loc[i]] = split_vals[i][j]  # Update the non-atomic value
            new_table.append(new_row)
    
    # Connect to the SQLite database and create a table
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create a table with columns from the header row
    header_row = new_table[0]
    columns = ', '.join(header_row)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS my_table ({columns})")

    # Insert rows into the table
    for i in range(1, len(new_table)):
        values = ', '.join([f"'{value}'" for value in new_table[i]])
        cursor.execute(f"INSERT INTO my_table VALUES ({values})")

    conn.commit()
    conn.close()

#   OLD CODE HERE. THIS RETURNS THE TABLE AS LIST OF LISTS
#   keeping just in case we want to change something for whatever reason

#   for i in range(len(split_vals)):
#       for j in range(len(split_vals[i])):
#           bad_rows[i][bad_loc[i]] = split_vals[i][j]
#           new_table.append(bad_rows[i])
#          
#   return new_table

# example usage:
if __name__ == "__main__":
    # Specify the input CSV file and the desired SQLite database filename
    input_csv_filename = 'exampleInputTable1.csv'
    output_db_filename = 'output.db'
    # Call the function to reorganize for 1NF and create the SQLite database
    reorganize_for_1NF(input_csv_filename, output_db_filename)
