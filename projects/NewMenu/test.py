from os import listdir
from new_menu import Menu
from string import ascii_lowercase, ascii_uppercase, digits
from time import sleep

a = ((ascii_lowercase + ascii_uppercase + " ") * 10).split(" ")[:-1]

print(a)

file = Menu(a).show()
print(file)