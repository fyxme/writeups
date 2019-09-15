> Inspect Me - Points: 125 - (Solves: 1155)
> Inpect this code! `http://2018shell1.picoctf.com:35349` (link)

We load the page and inspect the source.

In a comment we find:
`<!-- I learned HTML! Here's part 1/3 of the flag: picoCTF{ur_4_real_1nspe -->`

This looks very similar to a pico2017 challenge.

We find 2 resources:
- mycss.css
- myjs.js

We open both and we find our last 2 parts of the bottom of each.
`/* I learned CSS! Here's part 2/3 of the flag: ct0r_g4dget_098df0d0} */`
`/* I learned JavaScript! Here's part 3/3 of the flag:  */`

We combine all 3 parts and we get the flag.

Flag: `picoCTF{ur_4_real_1nspect0r_g4dget_098df0d0}`
