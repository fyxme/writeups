> roulette - Points: 350 - (Solves: 180)
> This Online Roulette Service is in Beta. Can you find a way to win $1,000,000,000 and get the flag? Source. Connect with nc 2018shell1.picoctf.com 48312


`uint64 vs long`
Long max: 9223372036854775807
Long max + 1 is negative

`9223372036854775808`

The number of money given at the start is also the value for the seed generator which mean you use the same seed and generate the same sequence of pseudo random values.

How to win:
- Win 3 times by putting a small bet value and using the calculated pseudo-random values
- After winning 3 times, loose once with value `3221215470` as bet

Flag: `picoCTF{1_h0p3_y0u_f0uNd_b0tH_bUg5_8fb4d984}`
