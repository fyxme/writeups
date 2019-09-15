> Super Safe RSA 2 - Points: 425 - (Solves: 292)
> Wow, he made the exponent really large so the encryption MUST be safe, right?! Connect with nc 2018shell1.picoctf.com 29661.

Large e values means d value will be small hence we can bruteforce it easily.

We find d = 65537

Flag: `picoCTF{w@tch_y0ur_Xp0n3nt$_c@r3fu11y_7736442}`
