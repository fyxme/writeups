#!/usr/bin/python3

import sys

print("Welcome to pysafe 3.0, please enter your password:")
pwd = input()
print 'pwd = ', pwd, ' || len(pwd) = ', len(pwd)
if (len(pwd) == 4):
    try:
        pwd = "".join([format(ord(a), "x") for a in pwd])
    except:
        pwd = pwd[::-1]
    print "pwd = ", pwd
    pwd = int(pwd, 16)
    print "pwd = ", pwd
else:
    sys.exit()
try:
    stuff = str(format(pwd, 'x'))[0:4]
    print "stuff = ", stuff
except:
    sys.exit()

print pwd%5
print pwd%6

# pwd = 5k + 4
# pwd = 6k' + 5
# pwd = 30k'' + 4k' + 5k
if((pwd%5 == 4 and pwd%6 == 5)):
    pwd = abs(pwd-300100111)
    print "pwd = ", pwd, " || len(pwd) = ", len(str(pwd))
else:
    sys.exit()

print "int(stuff) = ", int(stuff)
try:
    new_pwd = "".join([str(int(int(a)/2)) if int(int(stuff)/191+1) == len(str(pwd)) else sys.exit() for a in str(pwd)])

    for c in str(pwd):
        if int(int(stuff)/191+1) == len(str(pwd)):
            str(int(int(a)/2))
        else:
            sys.exit()
    # new_pwd = "".join([str(int(int(a)/2)) if int(int(stuff)/191+1) == len(str(pwd)) else sys.exit() for a in str(pwd)])

except:
    sys.exit()

if (int(new_pwd[4:]) == 1234):
    try:
        f=open("flag", "r")
        if f.mode == 'r':
            print(f.read())
    except:
        print("Victory!!! But flag not found, so that's weird")
