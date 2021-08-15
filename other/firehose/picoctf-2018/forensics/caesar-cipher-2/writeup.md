> caesar cipher 2 - Points: 250 - (Solves: 177)
> Can you help us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_1_ac88f1b12e9dbca252d450d374c4a087 on the shell server.

Caesar ciphers are only shifted characters which means if we find the offset of the first char to our plaintext, we can then use that same offset to decode the full cipher.

In this case they're using the ascii ordinal values of each later and offseting those by a certain amount.

By converting the ciphertext to it's ordinal equivalent, we see that the first char is of value 101.

We also know that the flag should start with "picoCTF..." and that "p" has for ordinal value 112.

Therefore the offset between the 2 is 11 (112-101 = 11).

We can add 11 to all the values of the cipher.txt to get the plaintext.

The file `exploit.py` is an implementation of the following.

And we get the plaintext `picoCTF{cAesaR_CiPhErS_juST_aREnT_sEcUrE}`

Flag: `picoCTF{cAesaR_CiPhErS_juST_aREnT_sEcUrE}`
