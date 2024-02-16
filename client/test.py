from data.Dat import *
import os, json
from cryptography.fernet import Fernet
f = f'{os.getcwd()}\\t.dat'
Dat.write({"users":[{"name":"felix","age":"30"},{"name":"josh","age":"32"}]},f)
# print(Dat.read(f))