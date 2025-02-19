def my_decorator(func):
    def wrapper():
        print("something before the function runs.")
        func()
        print("something after the function runs.")
    return wrapper
@my_decorator 
def say_hello():
    print("hello, world!")

say_hello()

# logging function calls 

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"calling function: {func.__name__}")
        return func (*args, **kwargs )
    return wrapper
@log_decorator
def greet(name):
    print(f"hello, {name}!")

greet("alice")

import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs )
        end = time.time()
        print(f"execution time:{end - start:.4f} seconds")
        return result
    return wrapper

@ timing_decorator
def slow_function():
    time.sleep(2)
    print("function completed")

slow_function()
# reload function

# mymodule.py

def greet():
    return "hello, world"
import mymodule
print(mymodule.greet())

# overloading and overriding

class mathoperations:
    def add(self, a, b, c=None):
        if c is not None:
            return a+b+c
        return a+b
obj = mathoperations()
print(obj.add(2,3))
print(obj.add(2,3,4))

class mathoperations:
    def add(self, *args):
        return sum(args)
obj = mathoperations()
print(obj.add(2,3))
print(obj.add(2,3,4))

#overriding
class animal:
    def speak(self):
        return "animal makes a sound"
class cat(animal):
    def speak(self):
        return "cat meows"
class dog(animal):
    def speak(self):
        return "cat meows"
dog =dog()
cat = cat()

print(dog.speak())
print(cat.speak())
 
class Employee:
    def __init__(self, name, salary):
        self._name = name
        self._salary = salary

    @property # getter
    def salary(self):
        return self._salary
    @salary.setter # setter
    def salary (self, value):
        if value > 0:
            self._salary = value
        else:
            raise ValueError("salary must be positive!")
  

emp = Employee("bob", 4000)

print(emp.salary)
emp.salary =5000

# modules

import math
print(math.sqrt(16))

# import specific functions
from math import sqrt
print(sqrt(15))

#import a module with an alias
import numpy as np 
array = np.array([1,2,3])
print(array)

# import everything from a module(not recommended)

from math import*
print(sin(90))

# finding module location

import math
print(math.__file__)

import sys 

print("python version:", sys.version)
print("executable path:", sys.executable)
print("system path:", sys.path)

from datetime import datetime, timedelta

now = datetime.now()
print("current date & time:", now)





