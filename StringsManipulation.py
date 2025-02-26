my_string = " Hello, world"
print(my_string)

print(my_string[0:3])
print(my_string[:-1])
print(my_string[-1:])
print(my_string[0:])
print(my_string[:0])

for i in my_string:
    print(i)

new_string= my_string + " this is hari"
print(new_string)

upper_case = my_string.upper()
lower_case = my_string.lower()
title_case = my_string.title()
print(upper_case)
print(lower_case)
print(title_case)

stripped_string = my_string.strip()
print(stripped_string)

my_set = {1,2,3,4,5}
my_set.add(6)
my_set.remove(5)
my_set.discard(4)
print(my_set)

is_in_set = 2 in my_set
print(is_in_set)

set1 = {1,2,3}
set2 = {3,4,5}
union_set = set1 | set2
intersection_set = set1 & set2
difference_set = set1 - set2
symmetric_difference_set = set1 ^ set2
print(union_set)
print(intersection_set)
print(difference_set)
print(symmetric_difference_set)
for i in my_set:
    print(i)

my_dict = {"name": "Alice", "age": 30, "city": "New York"}
name = my_dict["name"]
age = my_dict.get("age")
print(name)
print(age)
my_dict["email"] = "nanimanam"
print(my_dict)
