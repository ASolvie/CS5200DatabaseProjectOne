import os
import sqlite3
    
def create_table_query(tableName, keys) -> str:
    query = f'CREATE TABLE IF NOT EXISTS {tableName}('
    for ky in keys:
        query = f'{query}{ky} TEXT'
        if(keys[-1] != ky):
            query = f'{query},'
    query = f'{query})'
    return query

def find_primary_keys_in_relations(relations: dict) -> list[str]:
    keys = []
    values = []
    [keys.extend([x] if type(x) is str else list(x)) for x in list(relations.keys())]
    [values.extend([x] if type(x) is str else list(x)) for x in list(relations.values())]
    return [item for item in keys if item not in values]

def construct_create_table_query(tableName, keys, primaryKeys: list[str]) -> str:
    query = f'CREATE TABLE IF NOT EXISTS {tableName}('
    for x in keys:
        query = f'{query}{x} TEXT'
        if(x in primaryKeys):
            query = f'{query}'
        if(keys[-1] != x):
            query = f'{query},'
    if(len(primaryKeys) != 0):
        query = f'{query}, PRIMARY KEY ({",".join(primaryKeys)})'
    query = f'{query})'
    return query

def read_in_relations(filePath):
    file = open(f'{filePath}.txt', 'r')
    relations = []
    for x in file:
        keys,values = x.strip('\n').split('->')
        relations[tuple(keys.split(','))] = tuple(values.split(','))
    return relations

def readInMVDs(filePath):
    file = open(f'{filePath}.txt', 'r')
    MVDs = []
    for x in file:
        keys,values = x.strip('\n').split('-->')
        MVDs[tuple(keys.split(','))] = tuple(values.split(','))
    return MVDs

def delete_table_query(tableName) -> str:
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
        revisedFileName = file_name.strip('.csv')
        file = open(f'data/{folder_name}/{file_name}','r')
        names = file.readline().strip('\n').split(',')
        queries.append(create_table_query(revisedFileName, names))
        for x in file:
            queries.append(insert_into_table(f'{revisedFileName}', x.strip('\n').split(',')))
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()
    for que in queries:
        print(que)
        cursor.execute(que)
    connection.commit()

def create_select_columns_from_old_table(new_table_name, old_table_name, columns) -> str:
    query = f'CREATE TABLE {new_table_name} AS SELECT DISTINCT'
    for column in columns:
        query = f'{query} {column}'
        if(columns[-1] != column):
            query = f'{query},'
    query = f'{query} FROM {old_table_name};'
    return query

def list_table_names(database_name) -> list[str]:
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()
    return [value[0] for value in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

def find_table_with_columns(database_name, columns) -> str:
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()
    table_names = list_table_names(database_name)
    for table_name in table_names:
        if(all(y in [data[0] for data in cursor.execute('SELECT * FROM {table_name}').description] for y in columns)):
            return table_name
        
def list_primary_keys_of_table(database_name, table_name) -> list[str]:
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()
    return [name[0] for name in cursor.execute(f'SELECT name FROM PRAGMA_TABLE_INFO({table_name}) WHERE pk >= 1').fetchall()]