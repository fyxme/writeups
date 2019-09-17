First things first, we run the `file` command in an attempt to get some info about the file.

```
% file littleschoolbus.bmp
littleschoolbus.bmp: PC bitmap, Windows 3.x format, 252 x 199 x 24
```

Grepping for flag in strings return nothing and the exiftool returns no usefull data.

Since it is a `bmp` image it might be interesting to look at the least significant bit (LSB) to check for encoded data.

Using a tool like [zsteg](https://github.com/zed-0xff/zsteg) allows we can look at LSB hidden data.

Running `zsteg littleschoolbus.bmp` gives us the following output:
```
imagedata           .. text: "~vusnljmkhifgXWWNNOVUV~}"
b1,lsb,bY           .. text: "flag{remember_kids_protect_your_headers_f5e8}"
b3,r,lsb,xY         .. file: very old 16-bit-int big-endian archive
b4,rgb,msb,xY       .. file: MPEG ADTS, layer I, v2, 112 kbps, 24 kHz, JntStereo
```

Flag: `flag{remember_kids_protect_your_headers_f5e8}`
