import sqlite3
import os

class Relation:
    # x -> y
    def __init__(self, xToY):
        self.x: str = xToY[0]
        self.y: str = xToY[1]

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

def normalize_2nf(connection, table_name, relations):
    first = "" 
    temp=[]
    relation_y_dict = {}
    primary_keys = findPrimaryKeys(relations)
    No_PFD=primary_keys
    cursor = connection.cursor()
    # Create separate tables for non-prime attributes
    for relation in relations:
        if relation.x in primary_keys:
            if relation.y not in relation_y_dict:
                relation_y_dict[relation.y] = [relation.x]
            else:
                relation_y_dict[relation.y].append(relation.x)
            if first == "":
                first = relation.x
                #print(first)
            if first!= relation.x:
               # print(relation.x, relation.y)
                if relation.x not in temp:
                    temp.append(relation.x)
                    temp.append(relation.y)
                else:
                    temp.append(relation.y)
                #print("\n", temp)
                
        else:
            if relation.x in temp:
                temp.append(relation.y)
    for relation in relation_y_dict:
        if all(primary_key in relation_y_dict for primary_key in primary_keys):
            No_PFD.append(relation)

    query = constructCreateTableQuery("key_table", No_PFD, primary_keys)
    cursor.execute(query)
    cursor.execute(f"INSERT INTO key_table SELECT {table_name}.{No_PFD[0]}, {table_name}.{No_PFD[1]} FROM {table_name};")
    removeColumns(connection, table_name, primary_keys[1])
    #Here i want to make a table with 
    query = constructCreateTableQuery(primary_keys[1], temp, primary_keys)
    cursor.execute(query)
    cursor.execute(f"INSERT INTO {primary_keys[1]} SELECT {table_name}.{temp[0]}, {table_name}.{temp[1]},{table_name}.{temp[2]},{table_name}.{temp[3]}, {table_name}.{temp[4]} FROM {table_name};")
    removeColumns(connection, table_name, primary_keys[1])
    # Commit the changes
    connection.commit()
    #print("\n", relation_y_dict)


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
try:
    os.remove('school.db') # removes old school.db file
except: 
    print('file not found')
connection = sqlite3.connect('school.db') # create a new students database file
cursor = connection.cursor() # creates a cursor to interact with the database

# creates a table called students
cursor.execute("""
CREATE TABLE IF NOT EXISTS
students(
    studentId TEXT,
    firstName TEXT,
    lastName TEXT,
    course TEXT,
    professor TEXT,
    professorEmail TEXT,
    courseStart TEXT,
    courseEnd TEXT
)
""")

# parses the file and adds the rows
file = open('data/exampleInputTable1.csv', 'r')
file.readline()
for x in file:
    studentId, firstName, lastName, course, professor, professorEmail, courseStart, courseEnd = x.strip('\n').split(",")
    query = f'INSERT INTO students VALUES (\'{studentId}\', \'{firstName}\', \'{lastName}\', \'{course}\', \'{professor}\', \'{professorEmail}\', \'{courseStart}\', \'{courseEnd}\')'
    print(query)
    cursor.execute(query)
file.close()

# sanity check to see the data was added to the students table
cursor.execute("SELECT * FROM students")
print(cursor.fetchall())

# commits the changes to the actual file. While they aren't commit it is a temporary change
connection.commit()

file = open('data/relations.txt', 'r')
relations = []
for x in file:
    relations.append(Relation(x.strip('\n').split('->')))

normalize_2nf(connection, 'students', relations)

print('')
print(f'Primary keys {findPrimaryKeys(relations)}')

file = open('data/exampleInputTable1.csv', 'r')
k = file.readline().strip('\n').split(',')
cursor.execute(constructCreateTableQuery('testTable', k, findPrimaryKeys(relations)))

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Print data from each table
for table_name in table_names:
    table_name = table_name[0]  # Extract the table name from the tuple
    cursor.execute(f"SELECT * FROM {table_name};")
    print(f"Table: {table_name}")
    for row in cursor.fetchall():
        print(row)
    print()

cursor.execute("SELECT * FROM testTable")
print(cursor.fetchall())
#input("Which normal form level would you like?")