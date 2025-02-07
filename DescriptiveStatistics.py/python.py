def check_age(age):
    if age >=18:
        print("You are eligible to vote")
    else:
        print("You are not eligible to vote")

# enter voter age manually

try:
    age=int(input("enter your age: "))
    check_age(age)

except ValueError:
    print("Please enter a valid number")
