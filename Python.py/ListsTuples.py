my_list = [1,2,3,4,5]
print(my_list[0:4])
my_list[0] = 10
print(my_list)
my_list.append(4)
my_list.insert(2,15)
print(my_list)
my_list.remove(10)
print(my_list)

print("Iterating over list:")
for element in my_list:
    print(element)

my_tuple = (10,20,30,40,50)

for element in my_tuple:
    print(element)