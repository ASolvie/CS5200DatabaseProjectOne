import helper
done = False
database_name = ""
while(not done):
    print("Input folder containing your database, example 1NF. This folder should be in the data folder.")
    print("Tables should only contain letters from the alphabet.")
    folder_name = input()
    database_name = folder_name
    try :
        helper.create_database_from_folders(folder_name, database_name)
        done = True
    except:
        print("Error occured")
done = False

print('Input Functional Dependencies, example "columnNameOne->columnNameTwo" type "exit" when you are finished')
foo = ''
relations: list[helper.Relation] = []
while(foo != 'exit'):
    relationString = input()
    try:
        relations.append(helper.Relation(foo.split('->')))
    except:
        print(f'Did not understand your relation. relation not added for input "{relationString}"')

print('Pick the normal form you would like "1","2","3","B","4","5"')
print('input "1"  "2"  "3"  "3.5" "4"  "5"')
print('means 1NF  2NF  3NF  BCNF  4NF  5NF')
choice = 0
while(not done):
    try:
        string_input = input("Choice: ")
        choice = float(string_input)
        if(choice is 1.0 or
           choice is 2.0 or
           choice is 3.0 or
           choice is 3.5 or 
           choice is 4.0 or 
           choice is 5.0):
            done = True
        else:
            raise Exception('Invalid input')
    except:
        print(f'Invalid input {string_input}')
done = False
print('Find the highest normal form of the input database?')
while(not done):
    try:
        choice_string = input('"1": Yes, "2": No')
        choice = int(choice_string)
        if(choice is 1 or choice is 2):
            done = True
        else:
            raise Exception('Invalid input')
    except:
        print(f'Invalid input {choice_string}')

if(choice >= 1.0):
    print('running 1NF')
if(choice >= 2.0):
    print('running 2NF')
if(choice >= 3.0):
    print('running 3NF')
if(choice >= 3.5):
    print('running BCNF')
if(choice >= 4.0):
    print('running 4NF')
if(choice >= 5.0):
    print('running 5NF')

