> hex editor - Points: 150 - (Solves: 520)
> This cat has a secret to teach you. You can also find the file in /problems/hex-editor_0_8c20f979e6b2740dee597871ff1a74ee on the shell server.

This is a "hex editor" challenge but `strings` already gives us all the ascii values in the file so we just need to run `strings` and we get the flag.

```
% strings hex_editor.jpg | grep pico
Your flag is: "picoCTF{and_thats_how_u_edit_hex_kittos_3E03e57d}"
```

Flag: `picoCTF{and_thats_how_u_edit_hex_kittos_3E03e57d}`
