> pipe - Points: 110 - (Solves: 808)
> During your adventure, you will likely encounter a situation where you need to process data that you receive over the network rather than through a file. Can you find a way to save the output from this program and search for the flag? Connect with 2018shell1.picoctf.com 2015.


We first run `nc 2018shell1.picoctf.com 2015` and soon realise that there is a lot of garbage data.

We pipe it through grep and ask for the flag. 
```
% nc 2018shell1.picoctf.com 2015 | grep picoCTF
picoCTF{almost_like_mario_8861411c}
```

Flag: `picoCTF{almost_like_mario_8861411c}`
