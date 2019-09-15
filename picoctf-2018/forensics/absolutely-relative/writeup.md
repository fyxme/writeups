> absolutely relative - Points: 250 - (Solves: 499)
> In a filesystem, everything is relative ¯\_(ツ)_/¯. Can you find a way to get a flag from this program? You can find it in /problems/absolutely-relative_3_c1a43555f1585c98aab8d5d2c7f0f9cc on the shell server. Source.

From the source file we can see that the permissions are being read from a permissions which is open relative to where the program has been executed.
`file = fopen( "./permission.txt" , "r");`

This mean we can create an arbitrary file in a folder we control and run the program from there. It will use the file we create to read the permissions from.

In order to get the flag printed we need to have a file with the permission "yes" as such:

```
nsa@pico-2018-shell-1:~$ echo "yes" > permission.txt
nsa@pico-2018-shell-1:~$ /problems/absolutely-relative_3_c1a43555f1585c98aab8d5d2c7f0f9cc/absolutely-relative
You have the write permissions.
picoCTF{3v3r1ng_1$_r3l3t1v3_6193e4db}
```

Flag: `picoCTF{3v3r1ng_1$_r3l3t1v3_6193e4db}`
