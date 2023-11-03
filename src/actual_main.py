import helper
import inputs
import FiveNF_Code
import Four_NF_Code
import BCNF_Code
import Three_NF_Code
import Two_NF_Code
import One_NF_Code
import sqlite3

#database_name = inputs.create_database()
#relations = inputs.create_relations()
#mvds = inputs.create_mvds()
#relations = helper.read_in_relations("relations")
print("Input dataset (.csv format):")
input_table = input()

with open("relations.txt", "w") as file:
    while True:
        inp = input("Input Functional Dependencies (type “exit” and hit enter to complete your dependency list):")
        if inp == "exit":
            break
        file.write(inp + "\n")

with open("Multivalued.txt", "w") as file:
    while True:
        inp = input("Input Multi-valued Dependencies (type “exit” and hit enter to complete your dependency list. Do not use whitespace/spaces):")
        if inp == "exit":
            break
        file.write(inp + "\n")
relations = helper.read_in_relations("relations")
print('Pick the normal form you would like "1","2","3","B","4","5"')
print('input "1"  "2"  "3"  "3.5" "4"  "5"')
print('means 1NF  2NF  3NF  BCNF  4NF  5NF')
choice = 0
done = False
while(not done):
    try:
        string_input = input("Choice: ")
        choice = float(string_input)
        if(choice == 1.0 or
           choice == 2.0 or
           choice == 3.0 or
           choice == 3.5 or 
           choice == 4.0 or 
           choice == 5.0):
            done = True
        else:
            raise Exception('Invalid input')
    except:
        print(f'Invalid input {string_input}')

#print('Find the highest normal form of the input database?')
#while(not done):
#    try:
#        choice_string = input('"1": Yes, "2": No')
#        choice = int(choice_string)
#        if(choice is 1 or choice is 2):
#            done = True
#        else:
#            raise Exception('Invalid input')
#    except:
#        print(f'Invalid input {choice_string}')

primary_keys = helper.find_primary_keys_in_relations(relations)
if(choice >= 1.0):
    One_NF_Code.reorganize_for_1NF(input_table, 'ddo')
if(choice >= 2.0):
    Two_NF_Code.normalize_2nf()
if(choice >= 3.0):
    Three_NF_Code.convert_to_3NF('ddo')
if(choice >= 3.5):
    BCNF_Code.convertToBCNF('ddo')
if(choice >= 4.0):
    Four_NF_Code.convertTo4NF('ddo')
if(choice >= 5.0):
    FiveNF_Code.fifth_normal_form('ddo.db', primary_keys)

# BELOW CODE IS MEANT TO OUTPUT CONTENT OF ddo.db TO OUTPUT FILE

# Connect to the SQLite database
conn = sqlite3.connect("ddo.db")
cursor = conn.cursor()

# Get a list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Open the output.txt file for writing
with open('output.txt', 'w') as output_file:
    # Iterate through the table names and generate CREATE TABLE statements
    for table_name in table_names:
        table_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        
        create_table_query = f"CREATE TABLE {table_name} ("
        for column in table_info:
            column_name = column[1]
            data_type = column[2]
            not_null = "NOT NULL" if column[3] else ""
            primary_key = "PRIMARY KEY" if column[5] else ""
            create_table_query += f"{column_name} {data_type} {not_null} {primary_key}, "
        create_table_query = create_table_query[:-2]  # Remove the trailing comma and space
        create_table_query += ");\n"
        
        # Write the CREATE TABLE statement to the output file
        output_file.write(create_table_query)

# Close the database connection
conn.close()
