import queue
from tkinter.tix import COLUMN
import helper
import sqlite3
import os
import string

def find_transitive_dependencies(relations: list[helper.Relation]) -> list[helper.Relation]:
    transitive_dependencies = []
    k = []
    for relation in relations:
        k.append(relation.x)
    for r in relations:
        if(r.y in k):
            transitive_dependencies.append(helper.Relation([r.x, r.y]))
    return transitive_dependencies
    
def convert_to_3NF(db_name):
    try:
        os.remove(f'{db_name}.db') # removes old ddo.db file, ddo is the new db file
    except: 
        print('file not found')
    
    helper.create_database_from_folders(db_name, "1NF")#takes the 1NF table since it is easiest to make into 3NF
    relations = helper.read_in_relations("data/relations")
    primary_keys = helper.find_primary_keys_in_relations(relations)
    
    transitive_deps = find_transitive_dependencies(relations)
    
    #print("Revised Functional Dependencies:", relations)
    #print("transitive dependency", transitive_deps)
    #print("Updated Primary Keys:", primary_keys)
    
    newTableNames = list(string.ascii_uppercase)
    
    # create tables from primary key relationss
    queries = []#the queries needed to make the new db
    n = 1#this keeps track of where we are in new table names so we do not duplicate table names, starts at one so the first letter is B and not A
    name = []
    for derp in primary_keys: #to make new tables for primary keys
        name.append([derp] + [value.y for value in relations if value.x == derp])
    
    for i in range (len(primary_keys)):
            queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))#makes the sql queries for a db file
            n = n + 1#increments the n variable
    
    
    # create tables from non primary key relations
    name = []
    for derp in transitive_deps: #this is to make tables for the transitive deps
        name.append([derp.y] + [value.y for value in relations if value.x == derp.y])
    for i in range (len(transitive_deps)):
            queries.append(helper.create_select_columns_from_old_table(f'{newTableNames[n]}', 'A', name[i]))#makes the sql queries for a db file
            n = n + 1
    
    queries.append(helper.delete_table_query('A'))#deletes the original table being given to make the db look better

    connection = sqlite3.connect(f'{db_name}.db')
    cursor = connection.cursor()
    for que in queries:
        (que)
        cursor.execute(que)
    connection.commit()
#convert_to_3NF("ddo")