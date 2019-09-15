> Ext Super Magic - Points: 250 - (Solves: 9)
> We salvaged a ruined Ext SuperMagic II-class mech recently and pulled the filesystem out of the black box. It looks a bit corrupted, but maybe there's something interesting in there. You can also find it in /problems/ext-super-magic_4_f196e59a80c3fdac37cc2f331692ef13 on the shell server.

Running the file command we see that the image is not recognised as an image file:
```
% file ext-super-magic.img
ext-super-magic.img: data
```

Running binwalk returns a very large number of files
```
% binwalk ext-super-magic.img | wc
    505    4012   33191
```

Running foremost we are able to extract 40 jpg images from it.


