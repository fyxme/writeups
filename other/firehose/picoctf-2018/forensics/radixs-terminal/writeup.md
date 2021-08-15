> Radix's Terminal - Points: 400 - (Solves: 467)
> Can you find the password to Radix's login? You can also find the executable in /problems/radix-s-terminal_2_4c75009af9dadb458328555d93a49198?

In the file we have an string like so `aCgljb0nurntiqx db 'cGljb0NURntiQXNFXzY0X2VOQ29EaU5nX2lTX0VBc1lfMjk1ODA5OTN9',0`

It looks likes a base64 string and by trying to decode it we can confirm it is indeed.
```
% echo 'cGljb0NURntiQXNFXzY0X2VOQ29EaU5nX2lTX0VBc1lfMjk1ODA5OTN9' | base64 --decode
picoCTF{bAsE_64_eNCoDiNg_iS_EAsY_29580993}
```

Flag: `picoCTF{bAsE_64_eNCoDiNg_iS_EAsY_29580993}`
