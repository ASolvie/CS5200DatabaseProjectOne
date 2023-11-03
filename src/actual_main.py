import helper
import inputs
import FiveNF_Code
import Four_NF_Code
import Three_NF_Code
import Two_NF_Code
import One_NF_Code

#database_name = inputs.create_database()
relations = inputs.create_relations()
mvds = inputs.create_mvds()

print("Input dataset (.csv format):")
input_table = input()

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

primary_keys = helper.find_primary_keys_in_relations(relations)
if(choice >= 1.0):
    One_NF_Code.reorganize_for_1NF(input_table, 'ddo.db')
if(choice >= 2.0):
    print('running 2NF')
if(choice >= 3.0):
    print('running 3NF')
if(choice >= 3.5):
    print('running BCNF')
if(choice >= 4.0):
    Four_NF_Code.convertTo4NF('ddo.db')
if(choice >= 5.0):
    print('running 5NF')
    FiveNF_Code.fifth_normal_form('ddo.db', primary_keys)

