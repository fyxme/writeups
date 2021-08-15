> caesar cipher 1 - Points: 150 - (Solves: 747)
> This is one of the older ciphers in the books, can you decrypt the message? You can find the ciphertext in /problems/caesar-cipher-1_2_73ab1c3e92ea50396ad143ca48039b86 on the shell server.

Since this is a Ceasar cipher we can bruteforce the whole keyspace and get the flag:
```
% python ceasar.py "payzgmuujurjigkygxiovnkxlcgihubb"
0 | payzgmuujurjigkygxiovnkxlcgihubb
1 | qbzahnvvkvskjhlzhyjpwolymdhjivcc
2 | rcabiowwlwtlkimaizkqxpmzneikjwdd
3 | sdbcjpxxmxumljnbjalryqnaofjlkxee
4 | tecdkqyynyvnmkockbmszrobpgkmlyff
5 | ufdelrzzozwonlpdlcntaspcqhlnmzgg
6 | vgefmsaapaxpomqemdoubtqdrimonahh
7 | whfgntbbqbyqpnrfnepvcuresjnpobii
8 | xighouccrczrqosgofqwdvsftkoqpcjj
9 | yjhipvddsdasrpthpgrxewtgulprqdkk
10 | zkijqweetebtsquiqhsyfxuhvmqsrell
11 | aljkrxffufcutrvjritzgyviwnrtsfmm
12 | bmklsyggvgdvuswksjuahzwjxosutgnn
13 | cnlmtzhhwhewvtxltkvbiaxkyptvuhoo
14 | domnuaiixifxwuymulwcjbylzquwvipp
15 | epnovbjjyjgyxvznvmxdkczmarvxwjqq
16 | fqopwckkzkhzywaownyeldanbswyxkrr
17 | grpqxdllaliazxbpxozfmeboctxzylss
18 | hsqryemmbmjbaycqypagnfcpduyazmtt
19 | itrszfnncnkcbzdrzqbhogdqevzbanuu
20 | justagoodoldcaesarcipherfwacbovv
21 | kvtubhppepmedbftbsdjqifsgxbdcpww
22 | lwuvciqqfqnfecguctekrjgthycedqxx
23 | mxvwdjrrgrogfdhvduflskhuizdferyy
24 | nywxeksshsphgeiwevgmtlivjaegfszz
25 | ozxyflttitqihfjxfwhnumjwkbfhgtaa
```

This seems to be the right rotation number: `20 | justagoodoldcaesarcipherfwacbovv`

Flag: `picoCTF{justagoodoldcaesarcipherfwacbovv}`
