> environ - Points: 150 - (Solves: 1107)
> Sometimes you have to configure environment variables before executing a program. Can you find the flag we've hidden in an environment variable on the shell server?

The env command returns all the environment variables with their values.

Simply grepping for pico returns the flag.

```
% env | grep pico
SECRET_FLAG=picoCTF{eNv1r0nM3nT_v4r14Bl3_fL4g_3758492}
```

Flag: `picoCTF{eNv1r0nM3nT_v4r14Bl3_fL4g_3758492}`
