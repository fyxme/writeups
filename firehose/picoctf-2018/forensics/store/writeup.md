> store - Points: 400 - (Solves: 486)
> We started a little store, can you buy the flag? Source. Connect with 2018shell1.picoctf.com 5795.

Simply running strings against the binary gives us the flag.

```
~/picoctf2018$ strings store  | grep picoCTF
YOUR FLAG IS: picoCTF{numb3r3_4r3nt_s4f3_dbd42a50}
```

