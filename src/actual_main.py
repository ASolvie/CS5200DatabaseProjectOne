import helper
import inputs

database_name = inputs.create_database()
relations = inputs.create_relations()
mvds = inputs.create_mvds()

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
    print('We expect tables to be in 1NF, because we limit what tables we parse.')
    helper.create_database_from_folders('foo','1NF')
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

