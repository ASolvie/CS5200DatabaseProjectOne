import sqlite3
import helper

# Helper function to split a table based on MVDs
def split_table(table_name, mvd: helper.Relation, cursor):
    if(table_name is None):
        return None
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get the attributes of the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Create new tables to store the split data
    new_table_name = f"{table_name}_{mvd.x}_{mvd.y}"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} ({mvd.x} TEXT, {mvd.y} TEXT)")

    # Populate the new tables
    for row in rows:
        x_value = row[columns.index(mvd.x)]
        y_values = row[columns.index(mvd.y)]
        cursor.execute(f"INSERT INTO {table_name}_{mvd.x}_{mvd.y} ({mvd.x}, {mvd.y}) VALUES (?, ?)", (x_value, y_values))

    # Remove original table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

def convertTo4NF(db_name):
    # Connect to your .db file
    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()

    # Initialize a list to store the multivalued dependencies
    multivalued_dependencies = helper.readInMVDs("data/Multivalued")
    
    # Create a list of all table names needed
    tables = []
    for a in multivalued_dependencies:
        tables.append(helper.find_table_with_columns(db_name, [a.x, a.y]))
        
    # Split all tables
    for table_name, mvd in zip(tables, multivalued_dependencies):
        split_table(table_name, mvd, cursor)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
