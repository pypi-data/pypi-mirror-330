from src.jmc import *

data = input("template data: ")
temp = Template.decompress(data)
print(repr(temp))
mod = Module([temp, temp])
print(repr(mod))