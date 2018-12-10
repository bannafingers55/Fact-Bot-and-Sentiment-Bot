import os
from bot import FilterBot
import tkinter as tk
import time

if os.path.isdir("data/") == False:
	print("Creating data directory")
	os.mkdir("data/")

try:
	f = open("data/token.data", "r")
	content = f.read()
	f.close()
except:
  f = open("data/token.data", "w+")
  token = input("Enter your token")
  f.write(token)
  f.close()


print("Booting...")

b = FilterBot()
b.run()
