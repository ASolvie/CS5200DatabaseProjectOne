import queue
from tkinter.tix import COLUMN
import helper
import sqlite3
import os
import string
#from num2words import num2words

try:
    os.remove('ddo.db') # removes old ddo.db file, ddo is the new db file
except: 
    print('file not found')

def find_transitive_dependencies(relations: list[helper.Relation]) -> list[helper.Relation]:
    transitive_dependencies = []
    k = []
    for relation in relations:
        k.append(relation.x)
    for r in relations:
        if(r.y in k):
            transitive_dependencies.append(helper.Relation([r.x, r.y]))
    return transitive_dependencies

def three_n_f(relations: list[helper.Relation], transitive_deps: list[helper.Relation]):
    for x in relations:
        for y in transitive_deps:
            if(x.x == y.y):
                relations.remove(x)
    return relations, transitive_deps

helper.create_database_from_folders("ddo", "1NF")#takes the 1NF table since it is easiest to make into 3NF
relations = helper.read_in_relations("data/relations")
primary_keys = helper.find_primary_keys_in_relations(relations)

transitive_deps = find_transitive_dependencies(relations)

print("Revised Functional Dependencies:", relations)
print("transitive dependency", transitive_deps)
print("Updated Primary Keys:", primary_keys)

# create primary key table
primary_keys_query = helper.construct_create_table_query(1, primary_keys, [])
newTableNames = list(string.ascii_uppercase) #[num2words(i) for i in range(1, 26)] use this if the letters don't work

# create tables from primary key relationss
queries = []#the queries needed to make the new db
#output_queries = []####i believe this is what is needed for our project but not sure
n = 1#this keeps track of where we are in new table names so we do not duplicate table names, starts at one so the first letter is B and not A
name = []
for derp in primary_keys: #to make new tables for primary keys
    name.append([derp] + [value.y for value in relations if value.x == derp])

for i in range (len(primary_keys)):
        queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))#makes the sql queries for a db file
#        output_queries.append(helper.create_table_query(f'{newTableNames[n]}', name[i]))####makes the sql queries for the txt file to be outputted
        n = n + 1#increments the n variable


# create tables from non primary key relations
name = []
for derp in transitive_deps: #this is to make tables for the transitive deps
    name.append([derp.y] + [value.y for value in relations if value.x == derp.y])
for i in range (len(transitive_deps)):
        queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))#makes the sql queries for a db file
#        output_queries.append(helper.create_table_query(f'{newTableNames[n]}', name[i]))####makes the sql queries for the txt file to be outputted
        n = n + 1

# = list(string.ascii_uppercase)
queries.append(helper.delete_table_query('A'))#deletes the original table being given to make the db look better
#for i in range (n):
#    queries.append(f'ALTER TABLE {newTableNames[i]} RENAME TO {newerTableNames[i+1]};')#this was to make table names one, two, etc to B, C, D, etc, probably just needs deleted

connection = sqlite3.connect("ddo.db")
cursor = connection.cursor()
for que in queries:
    print(que)
    cursor.execute(que)
connection.commit()

#for i in range (len(output_queries)):####just prints the output queries to be reviewed
#    print(output_queries[i])####
