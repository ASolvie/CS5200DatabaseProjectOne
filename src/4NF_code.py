import sqlite3
import helper

# Helper function to split a table based on MVDs
def split_table(table_name, mvd: list[helper.Relation], cursor):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get the attributes of the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Create new tables to store the split data
    for dep in mvd:  
        new_table_name = f"{table_name}_{dep.x}_{dep.y}"
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} ({dep.x} TEXT, {dep.y} TEXT)")

    # Populate the new tables
    for row in rows:
        for dep in mvd:
            x_value = row[columns.index(dep.x)]
            y_values = row[columns.index(dep.y)]

            for y_value in y_values:
                cursor.execute(f"INSERT INTO {table_name}_{mvd.x}_{mvd.y} ({mvd.x}, {mvd.y}) VALUES (?, ?)", (x_value, y_value))

    # Remove original table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
def convertTo4NF(db_name):
    
    # Connect to your .db file
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Initialize a dictionary to store functional dependencies and multivalued dependencies
    multivalued_dependencies = helper.readInMVDs("data/Multivalued")
    
    # Create a list of all table names needed
    tables = []
    for a in multivalued_dependencies:
        tables.append(helper.find_table_with_columns(db_name, [a.x, a.y]))

    # Check if the table has multivalued dependencies
    for table_name, mvd in zip(tables, multivalued_dependencies):
        split_table(table_name, mvd, cursor)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
