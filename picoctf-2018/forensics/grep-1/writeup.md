> grep 1 - Points: 75 - (Solves: 1492)
> Can you find the flag in file? This would be really obnoxious to look through by hand, see if you can find a faster way. You can also find the file in /problems/grep-1_2_ee2b29d2f2b29c65db957609a3543418 on the shell server.

As the title of the challenge suggest, we grep the file for "picoCTF" and we get the flag.
```
% strings file | grep picoCTF
picoCTF{grep_and_you_will_find_42783683}
```

Flag: `picoCTF{grep_and_you_will_find_42783683}`

