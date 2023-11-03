import sqlite3
import os

class Relation:
    # x -> y
    def __init__(self, xToY):
        self.x: str = xToY[0]
        self.y: str = xToY[1]
def constructCreateTableQuery(tableName, keys, primaryKeys):
    query = f'CREATE TABLE IF NOT EXISTS {tableName}('
    for x in keys:
        query = f'{query}{x} TEXT'
        if(x in primaryKeys):
            query = f'{query} KEY'
        if(keys[-1] != x):
            query = f'{query},'

    query = f'{query})'
    return query
def findPrimaryKeys(relations: list[Relation]):
    k = []
    for r in relations:
        k.append(r.x)
    means = []
    for r in relations:
        means.append(r.y)
    for m in means:
        if(m in k):
            k.remove(m)
    return list(set(k))
def remove_duplicate_rows(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS temp_table AS SELECT DISTINCT * FROM {table_name};")
    cursor.execute(f"DELETE FROM {table_name};")
    cursor.execute(f"INSERT INTO {table_name} SELECT * FROM temp_table;")
    cursor.execute("DROP TABLE temp_table;")
    connection.commit()

def removeColumns(connection, table1, table2):
    cursor = connection.cursor()
    
    # Get the list of columns in the students table
    cursor.execute(f"PRAGMA table_info({table1})")  #
    student_columns = [column[1] for column in cursor.fetchall()]
    
    # Get the list of columns in the course table
    cursor.execute(f"PRAGMA table_info({table2})")  
    course_columns = [column[1] for column in cursor.fetchall()]

    # Identify the common columns between students and course tables
    columns_to_remove = [column for column in student_columns if column in course_columns]
    
    # Generate the ALTER TABLE query to remove the common columns
    for column in columns_to_remove:
        cursor.execute(f"ALTER TABLE {table1} DROP COLUMN {column}")
    
    # Commit the changes
    connection.commit()
def transform_relationships(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            x, y = line.split(' -> ')
            y_parts = [part.strip() for part in y.split(',')]
            
            if ',' in x:
                x_parts = [part.strip() for part in x.split(',')]
                for x_part in x_parts:
                    for y_part in y_parts:
                        outfile.write(f"{x_part}->{y_part}\n")
            else:
                for y_part in y_parts:
                    outfile.write(f"{x}->{y_part}\n")

def normalize_2nf():
    connection = sqlite3.connect('ddo.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #table_name = cursor.fetchall()
    yeet = cursor.fetchone()
    table_name = yeet[0]
    print(table_name)
    transform_relationships("data/relations.txt", "data/relations2.txt")
    file = open('data/relations2.txt', 'r')
    relations = []
    for x in file:
        relations.append(Relation(x.strip('\n').split('->')))

    first = "" 
    temp = []
    relation_x_dict = {}
    relation_x_dict2 = {}
    primary_keys = findPrimaryKeys(relations)
    No_PFD = primary_keys
    # Create a dictionary to group 'x' attributes that lead to the same 'y' attribute
    grouped_x_attributes = {}

    for relation in relations:
        x, y = relation.x, relation.y

        if y not in grouped_x_attributes:
            grouped_x_attributes[y] = [x]
        else:
            grouped_x_attributes[y].append(x)

    for y, x_attributes in grouped_x_attributes.items():
        # Create a combined 'x' key using a delimiter
        combined_x_key = '_'.join(sorted(x_attributes))

        if combined_x_key not in relation_x_dict:
            relation_x_dict[combined_x_key] = x_attributes
    for relation in relations:
        if relation.x in primary_keys:
            if relation.x not in relation_x_dict2:
                relation_x_dict2[relation.x] = [relation.y]
            else:
                relation_x_dict2[relation.x].append(relation.y)
            if first == "":
                first = relation.x
            if first != relation.x:
                if relation.x not in temp:
                    temp.append(relation.x)
                    if relation.y not in temp:
                        temp.append(relation.y)
                else:
                    if relation.y not in temp:
                        temp.append(relation.y)
    # Create tables for attributes in relation_x_dict
    for table_name2 in relation_x_dict:
        attributes = relation_x_dict[table_name2]

        for key, table_name3 in grouped_x_attributes.items():
            if len(table_name3) == 1 and table_name3[0] == table_name2:
                attributes.append(key)
        # Create the table
        query = constructCreateTableQuery(table_name2, attributes, primary_keys)
        cursor.execute(query)

        # Copy data from the original table to the new table
        attribute_list = ', '.join(attributes)
        #print(attribute_list)
        #print(table_name2)
        cursor.execute(f"INSERT INTO {table_name2} SELECT {table_name}.{attribute_list} FROM {table_name};")

        # Remove the copied columns from the original table
        removeColumns(connection, table_name, attributes)
        remove_duplicate_rows(connection, table_name2)

    # Commit the changes
    connection.commit()
