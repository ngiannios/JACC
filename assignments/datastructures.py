# simple_list = [1,2,3,4]
# a,b,c,d  = simple_list
# simple_list.extend([5,6,7])
# print(simple_list)
# del(simple_list[0])
# print(simple_list)

# d = {'name': 'Max', 'Telephone': '076'}
# print(d.items())
# print([el for (k,el) in d.items()])

# for k,v in d.items():
#     print(k,v)
# del(d['name'])
# print(d.items())

# t = (1,2,3)
# print(t.index(1))

# s={'Max', 'Anna', 'Max'}
# print(s)
# print ([el for el in s])

# new_list = [True, True, False]
# any(new_list)
# all(new_list)

# number_list = [1,2,3,-5]
# print(any([el>0 for el in number_list]))
# print(all([el>0 for el in number_list]))
def unlimited_arguments(*args, **kargs):
    print(kargs)
    for k ,argument in kargs.items():
        print(k , argument)

unlimited_arguments(1,2,3,4,5, name='Max', age='29')
print(*[1,2,3,4])