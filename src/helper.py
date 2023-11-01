import os
import sqlite3
def create_table_query(tableName, k):
    query = f'CREATE TABLE IF NOT EXISTS {tableName}('
    for x in k:
        query = f'{query}{x} TEXT'
        if(k[-1] != x):
            query = f'{query},'
    query = f'{query})'
    return query

class Relation:
    # x -> y
    def __init__(self, xToY):
        self.x: str = xToY[0]
        self.y: str = xToY[1]
    def __str__(self):
        return f'{self.x} to {self.y}'
    def __repr__(self):
        return f'{self.x} to {self.y}'
    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

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

def insert_into_table(tableName: str, values: list[str]) -> str:
    query = f'INSERT INTO {tableName} VALUES('
    for v in values:
        query = f'{query} \'{v}\''
        if(values[-1] != v):
            query = f'{query},'
    query = f'{query})'
    return query

def create_database_from_folders(database_name: str, folder_name: str):
    file_names = os.listdir(f'data/{folder_name}')
    queries = []
    for file_name in file_names:
        file = open(f'data/{file_name}','r')
        names = file.readline().strip('\n').split(',')
        queries.append(create_table_query(file_name, names))
        for x in file:
            queries.append(insert_into_table(file_name, x.strip('\n'.split(','))))
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cur