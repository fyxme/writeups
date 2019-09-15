> in out error - Points: 275 - (Solves: 687)
> Can you utlize stdin, stdout, and stderr to get the flag from this program? You can also find it in /problems/in-out-error_4_c51f68457d8543c835331292b7f332d2 on the shell server


The program asks us to print "Please may I have the flag?" to stdin.

By doing so we get a bunch of text which somewhat look like a flag... 

To search within that text we can grep for picoCTF and get what we were looking for.

```
$ python -c "print 'Please may I have the flag?'" | ./in-out-error | grep pico
picoCTF{p1p1ng_1S_4_7h1ng_f37fb67e}picoCTF{p1p1ng_1S_4_7h1ng_f37fb67e}picoCTF{p1p1ng_1S_4_7h1ng_f37fb67e}picoCTF{p1p1ng_1S_4_7h1ng_f37fb67e}
...
```

Flag: `picoCTF{p1p1ng_1S_4_7h1ng_f37fb67e}`
