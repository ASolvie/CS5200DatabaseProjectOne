import helper

def find_transitive_dependencies(relations: list[helper.Relation]) -> list[helper.Relation]:
    transitive_dependencies = []
    k = []
    for relation in relations:
        k.append(relation.x)
    for r in relations:
        if(r.y in k):
            transitive_dependencies.append(helper.Relation([r.x, r.y]))
    return transitive_dependencies

relations = helper.readInRelations("data/relations")
primary_keys = helper.findPrimaryKeys(relations)

transitive_deps = find_transitive_dependencies(relations)

for x in relations:
    for y in transitive_deps:
        if(x.x == y.y):
            relations.remove(x)
print("Revised Functional Dependencies:", relations)
print("transitive dependency", transitive_deps)
print("Updated Primary Keys:", primary_keys)

# create primary key table
primary_keys_query = helper.constructCreateTableQuery(1, primary_keys, [])

# create tables from primary key relations

# create tables from non primary key relations