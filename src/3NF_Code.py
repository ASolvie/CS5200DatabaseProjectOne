import queue
import helper
import sqlite3

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

relations = helper.readInRelations("data/relations")
primary_keys = helper.findPrimaryKeys(relations)

transitive_deps = find_transitive_dependencies(relations)
#relations, transitive_deps = three_n_f(relations, transitive_deps)

print("Revised Functional Dependencies:", relations)
print("transitive dependency", transitive_deps)
print("Updated Primary Keys:", primary_keys)

# create primary key table
primary_keys_query = helper.constructCreateTableQuery(1, primary_keys, [])
tableNames = ['one','two','three','four']

# create tables from primary key relations
name = []
for derp in primary_keys: 
    name.append([derp] + [value.y for value in relations if value.x == derp])
queries = []
for i in range (len(primary_keys)):
        queries.append(helper.create_table_query(f'{tableNames[i]}', name[i]))

# create tables from non primary key relations
name = []
for derp in transitive_deps: 
    name.append([derp.y] + [value.y for value in relations if value.x == derp.y])
for i in range (len(transitive_deps)):
        queries.append(helper.create_table_query(f'{tableNames[i + 2]}', name[i]))


connection = sqlite3.connect("test")
cursor = connection.cursor()
for que in queries:
    print(que)
    cursor.execute(que)
connection.commit()