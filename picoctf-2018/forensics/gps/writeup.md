> gps - Points: 550 - (Solves: 115)
> You got really lost in the wilderness, with nothing but your trusty gps. Can you find your way back to a shell and get the flag? Connect with nc 2018shell1.picoctf.com 21755. (Source).

Leaked address max offset is:
`1337 - 1337/2 = 1337 - 668 = 669 = 0x29d`

Buffer size: `1000`

Idea: Nopsled buffer so the address given falls approximately in the buffer


Flag: `picoCTF{s4v3_y0urs3lf_w1th_a_sl3d_0f_n0ps_frckuxac}`
