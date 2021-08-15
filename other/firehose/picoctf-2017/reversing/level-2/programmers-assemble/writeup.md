We're looking to figure out what "XXXXXX" is suposed to be.


We want to return 1 which mean eax should be 1 at the end of the program.

Starting from the bottom we see that to jump to the "good:" flag, the `cmp $0xb790, %ebx` needs to be equal to 0. ie $ebx needs to be equal to 0xb790 (`je good`)

We also see that ecx starts out as `0x8` and ebx starts at 0.

Every loop iteration we `add ecx, ebx` which results to the operation : 
`ebx = ebx + ecx`

Since ecx = 0x8 and does not change,
we have `ebx = ebx + 0x8`

We can generalise this to `ebx = 0 + 0x8 * n` where n is an integer which represents the number of iterations of the loop.

We need to find `ebx = 0xb790` to find the number of iterations required to return 1

`0xb790 / 8 = 5874 = 0x16f2`

eax represents the number of iterations of the loop (ie. `n`)

Therefore we need eax to start off as `0x16f2` which is the value of the flag

Flag: `0x16f2`
