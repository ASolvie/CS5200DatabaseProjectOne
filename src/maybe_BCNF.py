import sqlite3
import helper

# Helper function to determine if X is a superkey
def is_superkey(table_name, x, cursor):
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()
    
    # Check if X is a superkey by examining foreign keys
    for fk in foreign_keys:
        if x in fk:
            return True
    return False

# Helper function to split a table based on functional dependencies
def split_table(table_name, fds: helper.Relation, cursor):
    if table_name is None:
        return None
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Get the attributes of the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    if not is_superkey(table_name, fds.x, cursor):
        new_table_name = f"{table_name}_{fds.x}_key"
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} ({fds.x} TEXT PRIMARY KEY)")
        for row in rows:
            x_value = row[columns.index(fds.x)]
            cursor.execute(f"INSERT OR IGNORE INTO {new_table_name} ({fds.x}) VALUES (?)", (x_value,))

    new_table_name = f"{table_name}_{fds.x}_{fds.y}"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table_name} ({fds.x} TEXT, {fds.y} TEXT)")
    
    for row in rows:
        x_value = row[columns.index(fds.x)]
        y_value = row[columns.index(fds.y)]
        cursor.execute(f"INSERT INTO {new_table_name} ({fds.x}, {fds.y}) VALUES (?, ?)", (x_value, y_value))

    # Remove the original table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

def convertToBCNF(db_name):
    # Connect to your .db file
    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()

    # Initialize a list to store the functional dependencies
    functional_dependencies = helper.read_in_relations("relations")  # Replace with the actual path

    # Create a list of all table names needed
    tables = []
    for fd in functional_dependencies:
        tables.append(helper.find_table_with_columns(db_name, [fd.x, fd.y]))

    # Split all tables
    for table_name, fds in zip(tables, functional_dependencies):
        split_table(table_name, fds, cursor)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()