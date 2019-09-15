> Truly an Artist - Points: 200 - (Solves: 378)
> Can you help us find the flag in this Meta-Material? You can also find the file in /problems/truly-an-artist_4_cdd9e325cf9bacd265b98a7fe336e840.

The description talks about Meta-Material so we can assume we have to check the meta-tags of the image.

Using exiftool we can look at all the meta-tags for a supplied file. We use grep to find the flag and we get:
```
% exiftool 2018.png | grep picoCTF
Artist                          : picoCTF{look_in_image_13509d38}
```

Flag: `picoCTF{look_in_image_13509d38}`

