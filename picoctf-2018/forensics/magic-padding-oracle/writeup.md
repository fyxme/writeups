> Magic Padding Oracle - Points: 450 - (Solves: 40)
> Can you help us retreive the flag from this crypto service? Connect with nc 2018shell1.picoctf.com 24933. We were able to recover some Source Code.


Decrypted cookie:
```

Encrypted word was : {"username": "guest", "expires": "2000-01-07", "is_admin": "false"} 
Intermediate values: [[47, 74, 28, 0, 69, 27, 29, 65, 12, 11, 2, 115, 118, 22, 82, 67], [179, 185, 126, 10, 175, 8, 37, 7, 233, 36, 125, 183, 43, 228, 253, 33], [96, 165, 41, 66, 196, 110, 234, 201, 96, 39, 56, 55, 183, 111, 77, 115], [40, 90, 190, 86, 206, 193, 239, 206, 213, 192, 171, 241, 180, 49, 213, 162], [186, 23, 203, 101, 241, 180, 50, 13, 182, 11, 100, 40, 109, 174, 243, 213]]

```

<TODO>

```
% nc 2018shell1.picoctf.com 24933

Welcome to Secure Encryption Service version 1.51

Here is a sample cookie: 5468697320697320616e204956343536d6ca0a2883280762915414c54e97df1b40871b72f45ec7f9510a080095436d514129e137aaac86a0f7fa8bd3d250b9d1df35b668fcb93f00bb06692560a3fed8a3b523d385f1477b6daac14ff2416c67
What is your cookie?
c752165b7740ddc7db88a63f168744d70b9e78edd3301f0a525b6b0a1ed7ebe0797b8ed86988b6e9bee84ade1b03c546b58925ebc356ac28d009dadc1339b85841414141414141414141414141414141
username: a
Admin? true
Cookie is not expired
The flag is: picoCTF{0r4cl3s_c4n_l34k_ae6a1459}
```


Flag: `The flag is: picoCTF{0r4cl3s_c4n_l34k_ae6a1459}`
