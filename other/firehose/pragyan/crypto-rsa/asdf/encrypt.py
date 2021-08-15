from Crypto.Util.number import *
import random
import sys

def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

print sys.getrecursionlimit()

p = getPrime(512)
q = nextPrime(p+1)
while p%4 != 3 or q%4 !=3: # p = 4k + 3 | q = 4k' + 3
    p = getPrime(512)
    q = nextPrime(p+1)

print p
print q

exit()

n = p*q # % 4
m = open('secret.txt').read()
m = bytes_to_long(m)

m = m**e
c = (m*m)%n
c = long_to_bytes(c)
c = c.encode('hex')

cipherfile = open('ciphertext.txt','w')
cipherfile.write(c)

# 4f741fe93dd7e383ff527caa9a2f27d27fd74b53b62123837b74a2b024d0fbbe052f3b330ce5208ba989fc68e2f5235ac4e9dd9e091e7cb80c02745d9b2aad10cab9431590ae63117ce539ebf747b4bc81f2a293aea52f0b1fee746158dc45d0c8d60769a8a8e671fb049b52669a010a1ca6f5de851d715bf1821d8771bbeb47
