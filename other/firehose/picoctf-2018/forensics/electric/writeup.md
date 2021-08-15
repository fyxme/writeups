> eleCTRic - Points: 400 - (Solves: 128)
> You came across a custom server that Dr Xernon's company eleCTRic Ltd uses. It seems to be storing some encrypted files. Can you get us the flag? Connect with nc 2018shell1.picoctf.com 61333. Source.

AES CTR with nonce reuse

# electric
AES-CTR

plaintext is not padded
therefore len(plaintext) = len(cipher text)

Since you encrypt the `nonce + counter` and not the plaintext, it is possible to get the intermediate state if we pass in \x00 chars which will be xored with the intermediate state and therefore reveal it


since the ctr is only generated the first time we can get the intermediate state and then use that to encrypt arbitrary files

Flag file to decrypt is 29 in length:
```
len(“flag_547638ca36baee42a69b.txt”) = 29
```

1. Send 29 bytes of input to be encrypted
2. xor encrypted value with plaintext to get intermediate state
3. We can now create our own messages using intermediate state
    1. We xor the flag filename with the intermediate state and b64 encode it
    2. we then ask to decrypt a file and send the b64 encoded flag text we just created


Flag: `picoCTF{alw4ys_4lways_Always_check_int3grity_6c094576}`

