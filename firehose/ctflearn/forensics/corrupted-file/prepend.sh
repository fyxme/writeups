(perl -e 'print "\x47\x49\x46\x38\x39\x61\xe0"') | cat - unopenable.gif  > /tmp/out && mv /tmp/out fixed-unopenable.gif
