import queue
from tkinter.tix import COLUMN
import helper
import sqlite3
import os
from num2words import num2words

try:
    os.remove('ddo.db') # removes old ddo.db file
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

helper.create_database_from_folders("ddo", "1NF")
relations = helper.read_in_relations("data/relations")
primary_keys = helper.find_primary_keys(relations)

transitive_deps = find_transitive_dependencies(relations)

print("Revised Functional Dependencies:", relations)
print("transitive dependency", transitive_deps)
print("Updated Primary Keys:", primary_keys)

# create primary key table
primary_keys_query = helper.construct_create_table_query(1, primary_keys, [])
newTableNames = [num2words(i) for i in range(1, 11)]#['one','two','three','four'] use this list if num2words doesn't work

# create tables from primary key relationss
queries = []
n = 0
name = []
for derp in primary_keys: 
    name.append([derp] + [value.y for value in relations if value.x == derp])

for i in range (len(primary_keys)):
        queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))
        n = n + 1
n = i + 1 #to make sure we stay on the same count of new table names

# create tables from non primary key relations
name = []
for derp in transitive_deps: 
    name.append([derp.y] + [value.y for value in relations if value.x == derp.y])
for i in range (len(transitive_deps)):
        queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))
        n = n + 1

queries.append(helper.delete_table_query('A'))
connection = sqlite3.connect("ddo.db")
cursor = connection.cursor()
for que in queries:
    print(que)
    cursor.execute(que)
connection.commit()