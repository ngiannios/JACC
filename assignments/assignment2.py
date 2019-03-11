# 1) Create a list of names and use a for loop to output the length of each name (len()).
# 2) Add an if check inside the loop to only output names longer than 5 characters.
# 3) Add another if check to see whether a name includes a “n” or “N” character.
# 4) Use a while loop to empty the list of names (via pop())

list_of_names = ['Nikos', 'Tyree', 'Claudia', 'Mora', 'Lorna', 'Jen', 'Nina', 'Adrianne', 'Johnsie', 'Camille', 'Joleen', 'Lon', 'Evelyne', 'Sheilah', 'Galina', 'Rhea', 'Joesph', 'Alyce', 'Leanora', 'Laurena', 'Timmy']

for name in list_of_names:
    print(len(name))
    if (len(name) > 5):
        print(name)
    if 'n' in name or 'N' in name:
        print(name)
    
while len(list_of_names)>0:
    list_of_names.pop()

print(list_of_names)
