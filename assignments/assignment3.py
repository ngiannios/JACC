# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = []
persons.append( {
                'name': 'Nikos', 
                'age': '39', 
                'hobbies': {
                        'snowboarding', 'Play the piano', 'photography', 'diving'
                            }
                })
persons.append( {
                'name': 'Max', 
                'age': '21', 
                'hobbies': {
                        'blockchain', 'football', 'diving'
                            }
                })

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
print(
    [[name for key, name in l.items() if key == 'name'][0] for l in persons]
)

# 3) Use a list comprehension to check whether all persons are older than 20.

print(all(
    [[int(name)>20 for key, name in l.items() if key == 'age'][0] for l in persons])
)

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
copied_persons = [person.copy() for person in persons]
copied_persons[0]['name'] = 'Simi'
print(copied_persons)
print(persons)

# 5) Unpack the persons of the original list into different variables and output these variables.
p1, p2 = persons
print(p1)
print(p2)