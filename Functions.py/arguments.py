# arguments are values that are passed to a function when calling it
#positional arguments
def greet(name, age):
    print(f"hello {name}, you are {age} years old")
greet("hari", 25)
print(greet)
# default arguments
def greet(name="user", age="x"):
    print(f"hello {name}, you are {age} years old")
greet()
print(greet)
# keyword arguments
def greet(name, age):
    print(f"hello {name}, your age is {age}")
greet(age=25, name='kris')
print(greet)
# Variable-length arguments
def sum_numbers(*args):
    return sum(args)
print(sum_numbers(1,23,33))
print(sum_numbers(5, 10, 15, 20))
# Variable-length keyword arguments 
def display_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}:{value}")
display_info(name="alice", age=25, city="newyork")
