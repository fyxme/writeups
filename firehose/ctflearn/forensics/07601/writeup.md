1. running `strings` reveals strings which look like directory and file paths
2. Change name to `.zip` and unzip the file
3. cd to ./Secret Stuff.../Don't Open This...
4. run `hexdump -C <filename> | grep "ABCTF" -A 1` to get the flag: ABCTF{Du$t1nS_D0jo}

