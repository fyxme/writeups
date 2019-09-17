> """HELP BITY
60 points

43 solves

Miscellaneous

Medium

ioancristian

Bity had the flag for his problem. Unfortunately, his negative friend Noty corrupted it.
 Help Bity retrieve his flag. He only remembers the first 4 characters of the flag: CTFL. Flag: BUGMd`sozc0o`sx^0r^`vdr1ld|
"""

```
b = "BUGMd`sozc0o`sx^0r^`vdr1ld|"
a = '\x01' * len(b)
xored = [ord(c) ^ ord(d) for c,d in zip(a,b)]
xored = map(chr, xored)

print "".join(xored)
```


Flag: `CTFLearn{b1nary_1s_awes0me}`
