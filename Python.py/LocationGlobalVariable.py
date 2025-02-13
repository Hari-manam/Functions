# Local Variable 
def my_function():
    x=10 
    print(f"inside the function: x = {x}")

my_function()
# Global Variable
x=10
def my_function():
    print(f"outside the function x:{x}")
my_function()

# To modify a Global variable inside a function, use the global keyword
x=50

def my_function():
    global x
    x=10
    print(f"inside the function x={x}")
my_function()
print(f"outside the function x={x}")
