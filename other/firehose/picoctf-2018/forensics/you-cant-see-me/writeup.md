> you can't see me - Points: 200 - (Solves: 705)
> '...reading transmission... Y.O.U. .C.A.N.'.T. .S.E.E. .M.E. ...transmission ended...' Maybe something lies in /problems/you-can-t-see-me_1_a7045a1e39ce834c26556a81c2b3a74f.

The title suggest it might be a hidden file so we run `ls -la` to also print out hidden files that start with a '.' in unix.
```
% nsa@pico-2018-shell-1:/problems/you-can-t-see-me_1_a7045a1e39ce834c26556a81c2b3a74f$ ls -la
total 60
drwxr-xr-x   2 root       root        4096 Sep 28 08:29 .
-rw-rw-r--   1 hacksports hacksports    57 Sep 28 08:29 .
drwxr-x--x 576 root       root       53248 Sep 30 03:45 ..
```

There appears to be a hiden file.

By using tab autocompletion, we can print it's contents.
```
% cat ./.\ \
picoCTF{j0hn_c3na_paparapaaaaaaa_paparapaaaaaa_f01e45c4}
```

Flag: `picoCTF{j0hn_c3na_paparapaaaaaaa_paparapaaaaaa_f01e45c4}`
