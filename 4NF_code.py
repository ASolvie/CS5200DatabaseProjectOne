import sqlite3
import csv
import helper

# Helper function to split a table based on MVDs
def split_table(table_name, fd, mvd):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get the attributes of the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Create new tables to store the split data
    # TODO: fix this by fixing how MVDs are handled
    for X, Y in mvd:  # fix how MVDs are handled here
        new_table_name = f"{table_name}_{X}_{Y}"
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} ({X} TEXT, {Y} TEXT)")

    # Populate the new tables
    # TODO: fix this by fixing how MVDs are handled
    for row in rows:
        for X, Y in mvd:
            x_value = row[columns.index(X)]
            y_values = row[columns.index(Y)].split(',')  # fix how MVDs are handled here

            for y_value in y_values:
                cursor.execute(f"INSERT INTO {table_name}_{X}_{Y} ({X}, {Y}) VALUES (?, ?)", (x_value, y_value))

    # Remove original table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
def convertTo4NF(db_name):
    
    # Connect to your .db file
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Retrieve a list of all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Initialize a dictionary to store functional dependencies and multivalued dependencies
    functional_dependencies = helper.readInRelations("data/relations")
    multivalued_dependencies = helper.readInMVDs("data/Multivalued")

    # Iterate over the tables and process each one
    for table_name in tables:
        table_name = table_name[0]
    
        # Check if the table has multivalued dependencies
        if table_name in multivalued_dependencies:
            mvd = multivalued_dependencies[table_name]
    
            # Check if the table has functional dependencies
            if table_name in functional_dependencies:
                fd = functional_dependencies[table_name]
                split_table(table_name, fd, mvd)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
