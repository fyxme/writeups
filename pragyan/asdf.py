import random

file = open("secret.txt","r")
secret = file.read()

flag = ""
for i in secret:
    if i.isalpha():
        flag += i
l = len(flag)

# [[12313, 123142], [32983, 21389]]
key = [[int(random.random()*10000) for e in range(2)] for e in range(2)]

i = 0
ciphertext = ""


# vuqxyugfyzfjgoccjkxlqvguczymjhpmjkyzoilsxlwtmccclwizqbetwthkkvilkruufwuu
while i <= (l-2):
    x = ord(flag[i]) - 97
    y = ord(flag[i+1]) - 97
    z = (x*key[0][0] + y*key[0][1])%26 + 97
    w = (x*key[1][0] + y*key[1][1])%26 + 97 
    ciphertext = ciphertext + chr(z) + chr(w) # v u 
    i = i+2

cipherfile = open('ciphertext.txt','w')
cipherfile.write(ciphertext)

# pc tf
# ct f{

# z * z' = ('p' * key[0][0] + 'c'*key[0][1]) * ('t' * key[0][0] + 'f'*key[0][1])
# z * z' = key[0][0] * ('p' + 't') + key[0][1] * ('p' + 't')
# z * z' = (key[0][0] + key[0][1])%26 * ('p' + 't')%26

# z = x * (key[0][0])%26 + y * (key[0][1]) % 26 + 97
# w = (x*key[1][0] + y*key[1][1])%26 + 97

# z = (x*key[0][0] + y*key[0][1])%26 + 97
# w = (x*key[1][0] + y*key[1][1])%26 + 97
# z * w = (x*key[0][0] + y*key[0][1]) * (x*key[1][0] + y*key[1][1])
#       = (x*key[0][0] + y*key[0][1]) * (x*key[1][0]) 
#        +(x*key[0][0] + y*key[0][1]) * (y*key[1][1])




