import os

if os.path.exists("example.txt"):
    print("file exists")
else:
    print("file does not exists")

file= open ("example.txt", "r")
file.close()

with open("example.txt", "w") as file:
    file.write("hello, python\n")
    file.write("file handling is fun")

with open("example.txt","r") as file:
    content = file.read()
    print(content)

with open("example", "w") as file:
    file.write("some times i am getting an error doing file operations its because file directory is not present in the same directory\n")

with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())
with open("example.txt", 'r') as file:
    partial_content = file.read(10)
    print(partial_content)
with open("example.txt", "a") as file:
    file.write("\nappending new data")
    print("example.txt")
# a ensures the existing content is not deleted 

# writing an image 

with open("img.jpg", "rb") as file:
    data = file.read()

with open("img.jpg", "wb") as file:
    file.write(data)
    
