def createTable(tableName, cursor, k):
    query = f'CREATE TABLE IF NOT EXISTS {tableName}('
    for x in k:
        query = f'{query}{x} TEXT'
        if(k[-1] != x):
            query = f'{query},'
    query = f'{query})'
    cursor.execute(query)

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

def readInRelations(filePath):
    file = open(f'{filePath}.txt', 'r')
    relations = []
    for x in file:
        relations.append(Relation(x.strip('\n').split('->')))
    return relations

def deleteTable(tableName):
    return f'DROP TABLE {tableName}'

def insertIntoTable(tableName, values list[str]):
    query = f'INSERT INTO {tableName}'
    return query