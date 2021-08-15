> hertz - Points: 150 - (Solves: 355)
> Here's another simple cipher for you where we made a bunch of substitutions. Can you decrypt it? Connect with nc 2018shell1.picoctf.com 48186.

The description of the challenges tells us its a substitution cipher.

Firstly we extract the ciphertext using netcat.
`nc 2018shell1.picoctf.com 48186 > cipher.txt`

Using statistical analysis we can solve it easily. https://quipqiup.com/ is a great tool for it.

And we get the following flag from it.

Flag: `substitution_ciphers_are_solvable_ftcfvtwroh`
