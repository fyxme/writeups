# Web challenges for [ctf-name](https://ctf-name.com)

Useful command to convert directory names to links
`ll | grep -v "READ" | rev | cut -d" " -f1 | rev | sed -E 's/(.+)/[x] [\1](#) - [writeup](\1\/writeup.md)/'`

CTF difficulty: Intermediate
Number of Web Challenges: x

The writeups are listed below.

Challenges:
- [x] [Completed Challenge name](challenge link) - [writeup](challenge-name/writeup.md)
- [] [Not completed Challenge name](challenge link) - [writeup](challenge-name/writeup.md)