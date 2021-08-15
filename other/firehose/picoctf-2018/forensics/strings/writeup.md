> strings - Points: 100 - (Solves: 900)
> Can you find the flag in this file without actually running it? You can also find the file in /problems/strings_2_b7404a3aee308619cb2ba79677989960 on the shell server.

Using strings against the strings file we get:
```
% strings strings | grep pico
picoCTF{sTrIngS_sAVeS_Time_3f712a28}
```

Flag: `picoCTF{sTrIngS_sAVeS_Time_3f712a28}`
