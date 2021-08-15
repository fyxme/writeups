> hertz 2 - Points: 200 - (Solves: 220)
> This flag has been encrypted with some kind of cipher, can you decrypt it? Connect with nc 2018shell1.picoctf.com 12521.


This seems to be the continuation of hertz-1 so it's probably a substitution cipher.

Once again using https://quipqiup.com/ we do statistical analysis on the cipher.

It can't decrypt it fully on it's own but by manually decrypting a few letters/words we can help it fully analyse the cipher.

The manually defined "clues" are : ` j=p uqwgt=quick bhvkr=brown xvo=dog efzs=lazy aqdjy=jumps nvm=fox`

The decoded cipher:
```
    The quick brown fox jumps over the lazy dog. I can't believe this is such an easy problem in Pico. It's almost as if I solved a problem already! Okay, fine. Here's the flag: picoCTF{substitution_ciphers_are_too_easy_sgsgtnpibo}
```

Flag: `picoCTF{substitution_ciphers_are_too_easy_sgsgtnpibo}`
