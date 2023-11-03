import helper
import sqlite3
def fifth_normal_form(database_name, primary_keys: list[str]):
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()
    combinations = []
    queries = []
    for p in range(len(primary_keys)):
            for k in range(p+1, len(primary_keys)):
                combinations.append((primary_keys[p], primary_keys[k]))
    for c in combinations:
        queries.append(helper.create_table_query(f'FiveNF{c[0]}_{c[1]}', [c[0], c[1]]))
    [cursor.execute(query) for query in queries]
    connection.commit()
    connection.close()