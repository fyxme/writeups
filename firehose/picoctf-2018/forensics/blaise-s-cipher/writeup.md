> blaise's cipher - Points: 200 - (Solves: 324)
> My buddy Blaise told me he learned about this cool cipher invented by a guy also named Blaise! Can you figure out what it says? Connect with nc 2018shell1.picoctf.com 46966.

Blaise's cipher is refering to a Vignere cipher (Blaise de Vignere).

Using dcode.fr we can bruteforce the key using statistical analysis.

We find the key to be "flag".

Using cryptii.com we decode the cipher and get the flag. (decrypted cipher available in plain.txt)

Flag: `picoCTF{v1gn3r3_c1ph3rs_ar3n7_bad_cdf08bf0}`
