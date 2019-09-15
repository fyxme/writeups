We run the program and redirect the output to a file:
`./raw2hex > /tmp/out`

Using python we print the file data out as hex:


```python
with open('/tmp/out') as f:
    data = f.read()

print data.encode('hex')

```

By running the program we know the flag is after a double dot ':' which is equivalent to `0x3a` in hex

By looking at the output from the python script we stop at the first occurence of a 3a and use the rest of the output as the flag.

Flag: `0e3ab3cfb1a7db2c3d18428532c97b05`
