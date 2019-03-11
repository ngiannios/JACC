# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def normal_function(arg):
    print(arg())

def another_function():
    return 'This is the result of another function.'

normal_function(another_function)
# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.

normal_function(lambda : 'This is the lambda function.')
# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed. 
def normal_infinite_args_function(fn, *args):
    for arg in args:
        print(fn(arg))

normal_infinite_args_function(lambda  data : data / 5, 5, 10, 15, 20, 25)

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.

def normal_function_with_format(fn, *args):
    for arg in args:
        print('Result: {:^20.2f}'.format(fn(arg)))

normal_function_with_format(lambda  data : data / 5, 5, 10, 15, 20, 25)
