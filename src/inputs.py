import helper
def create_database():
    done = False
    while(not done):
        print("Input folder containing your database, example 1NF. This folder should be in the data folder.")
        print("Tables should only contain letters from the alphabet.")
        folder_name = input()
        database_name = folder_name
        try :
            helper.create_database_from_folders(folder_name, database_name)
            return database_name
        except:
            print("Error occured")
    done = False
    return None

def create_relations():
    print('Input Functional Dependencies, example "columnNameOne->columnNameTwo" type "exit" when you are finished')
    relation_string = ''
    relations = {}
    while(relation_string != 'exit'):
        relation_string = input()
        try:
            keys,values = relation_string.split('->')
            relations[tuple(keys.split(','))] = tuple(values.split(','))
        except:
            print(f'Did not understand your relation. relation not added for input "{relation_string}"')
    return relations

def create_mvds():
    print('Input Multi-valued Dependencies, example columnNameOne->>columnNameTwo, type "exit" when you are finished')
    mvd_string = ''
    mvds = {}
    while(mvd_string != 'exit'):
        mvd_string = input()
        try:
            key, value = mvd_string.split('->>')
            mvds[key] = value
        except:
            print(f'Did not understand you MVD. mvd not added for input "{mvd_string}"')