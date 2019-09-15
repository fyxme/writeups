>
> 

We start by loading the file in gdb by running `gdb ./run`.


We disassemble the program to get an address before main returns and we set a breakpoint at that location.

In this case I chose this address `b *0x0000000000400914`

We run the program and let it decrypt the flag.

Gdb will stop the program at the location we specified.

At this point we can simply print the value of `flag_buf` as a string
```
gef➤  x/s flag_buf
0x602010:       "picoCTF{gDb_iS_sUp3r_u53fuL_f3f39814}"
```

Flag: `picoCTF{gDb_iS_sUp3r_u53fuL_f3f39814}`
