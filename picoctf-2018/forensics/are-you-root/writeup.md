> are you root? - Points: 550 - (Solves: 134)
> Can you get root access through this service and get the flag? Connect with nc 2018shell1.picoctf.com 33149. Source.

first idea:
- login as a user with a name of length 64 + the number 5 for the auth level (128 bin will be allocated)
- reset the user
- login with a username less than 64 bytes (64 bin will be allocated) and the auth level will remain as it was specified before
- lastly show flag

<TODO>

Flag: `picoCTF{m3sS1nG_w1tH_tH3_h43p_28e2061f}`
