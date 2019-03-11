my_name = 'Nikos'
my_age = 39

def print_data(any_data):
    print(any_data)

def print_data2(data1, data2):
    print(data1+str(data2))

def number_of_decades(data):
    return int(my_age/10)

print_data(my_name)
print_data2(my_name, my_age)
print_data(number_of_decades(my_age))
