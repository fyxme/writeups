> what base is this? - Points: 200 - (Solves: 1000)
> To be successful on your mission, you must be able read data represented in different ways, such as hexadecimal or binary. Can you get the flag from this program to prove you are ready? Connect with nc 2018shell1.picoctf.com 64706.

The challenge is to convert from a base to it's ascii value.
The easiest way is to use python and to convert the given values to integers and then get the chr value of those integers.

The given bases are in this order:
- base 2
- base 16
- base 8

To convert from a base 2 string to a base 10 int in python simply supply the base as the second argument as such `int(s, base_num)`

Flag: `picoCTF{delusions_about_finding_values_5b21aa05}`
