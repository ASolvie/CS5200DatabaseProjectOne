import helper
def fifth_normal_form(primary_keys: list[str]):
    combinations = []
    queries = []
    for p in range(len(primary_keys)):
            for k in range(p+1, len(primary_keys)):
                combinations.append((primary_keys[p], primary_keys[k]))
    for c in combinations:
        queries.append(helper.create_table_query(f'FiveNF{c[0]}_{c[1]}', [c[0], c[1]]))
    return queries