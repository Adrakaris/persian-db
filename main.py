import sys
print(sys.version)

from tkinter import *
from functions import read_csv, linearly_find, write_csv, Table

# column names
TARG_LANG = 0
TARG_WORD = 1
ARIYA_SOURCE = 2
DEF = 3
TAVERNIER = 4
VARIANTS = 5
TYPE = 6
TRANSMISSION = 7
MED = 9
MEDIAN = 10

dictionary: Table[str]
HEADERS: str
dictionary, HEADERS = read_csv("persianDict.csv")

write_csv("test.csv", HEADERS, dictionary)

# for i in range(20):
#     print(dictionary[i])
