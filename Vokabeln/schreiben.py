import time, os, sys, random
lk = input("Welche Lektion möchtest du hinzufügen?\n")
try:
    xk = open(lk, "w")
except:
    print("ERROR")
    sys.exit()
