import sqlite3 as sql
import helper
def fifth_normal_form(database_name: str, primary_keys: list[str]):
    connection = sql.connect(f'{database_name}.db')
    cursor = connection.cursor()
    combinations = []
    queries = []
    for p in range(len(primary_keys)):
            for k in range(p+1, len(primary_keys)):
                combinations.append((primary_keys[p], primary_keys[k]))
    for c in combinations:
        queries.append(helper.create_table_query(f'FiveNF{c[0]}_{c[1]}', [c[0], c[1]]))
    print(queries)
    connection.commit()

print(fifth_normal_form('ddo', ['travelingSalesMan', 'productType', 'brand']))