> grep 2 - Points: 125 - (Solves: 1608)
> This one is a little bit harder. Can you find the flag in /problems/grep-2_1_ef31faa711ad74321a7467978cb0ef3a/files on the shell server? Remember, grep is your friend.

The first attempt was to use recursive grep `grep -rnw "pico" .`
Unfortunately, nothing was returned.

Changing the grep command slightly we recursively grep for "picoCTF" and we get the flag.

```
% grep -r "picoCTF"
./files9/file13:picoCTF{grep_r_and_you_will_find_4baaece4}
```
Flag: `picoCTF{grep_r_and_you_will_find_4baaece4}`
