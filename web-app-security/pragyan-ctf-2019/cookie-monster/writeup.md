> Do prepare to see cookies lurking everywhere.

Based on the challenge description, we start by looking at the cookies created when making a request.

We find a cookie called `flag` with a value which looks like a hash.

After exploring the source code and refreshing the page a few times, we can see that the cookie's value has changed.

It seems that after each refresh the cookie's value changes.

The value looks like a md5 hash. By using an online md5 database, we can see that the hash matches a 2 character value.

It seems that the cookie changes every page refresh and the md5 value corresponds to a 2 char value. Therefore, we're able to refresh the page until we get all the md5 values and crack the hash using a database such as `https://hashkiller.co.uk/`.

This gives us a list of hashes as such:

```
bc54f4d60f1cec0f9a6cb70e13f2127a MD5 pc
114d6a415b3d04db792ca7c0da0c7a55 MD5 tf
b2984e12969ad3a3a2a4d334b8fb385a MD5 {c
6f570c477ab64d17825ef2d2dfcb6fe4 MD5 0o
988287f7a1eb966ffc4e19bdbdeec7c3 MD5 ki
0d4896d431044c92de2840ed53b6fbbd MD5 3s
f355d719add62ceea8c150e5fbfae819 MD5 _@
12eccbdd9b32918131341f38907cbbb5 MD5 re
639307d281416ad0642faeaae1f098c4 MD5 _y
96bc320e4d72edda450c7a9abc8a214f MD5 Um
c716fb29298ad96a3b31757ec9755763 MD5 _b
51de5514f3c808babd19f42217fcba49 MD5 Ut
05cb7dc333ca611d0a8969704e39a9f0 MD5 _t
bc781c76baf5589eef4fb7b9247b89a0 MD5 HE
ff108b961a844f859bd7c203b7366f8e MD5 y_
2349277280263dff980b0c8a4a10674b MD5 @l
0b1cdc9fe1f929e469c5a54ffe0b2ed5 MD5 s0
364641d04574146d9f88001e66b4410f MD5 _r
c758807125330006a4375357104f9a82 MD5 3v
fcfdc12fb4030a8c8a2e19cf7b075926 MD5 Ea
440c5c247c708c6e46783e47e3986889 MD5 L_
97a7bf81a216e803adfed8bd013f4b85 MD5 @_
c1d12de20210d8c1b35c367536e1c255 MD5 l0
a8655da06c5080d3f1eb6af7b514e309 MD5 t}
```

We save them to a file called `out.txt` and using a simple bash one-liner we can extract the flag: `cat out.txt | cut -d" " -f3 | tr -d "\n"`

Flag: `pctf{c0oki3s_@re_yUm_bUt_tHEy_@ls0_r3vEaL_@_l0t}`
