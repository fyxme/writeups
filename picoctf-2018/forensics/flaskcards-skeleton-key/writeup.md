> Flaskcards Skeleton Key - Points: 600 - (Solves: 229)
> Nice! You found out they were sending the Secret_key: 385c16dd09098b011d0086f9e218a0a2. Now, can you find a way to log in as admin? http://2018shell1.picoctf.com:48263 (link).

Since we have flask app key we can encrypt and decrypt cookies at will.
This allows us to decrypt the session cookie and change our user id to 1 which is the admin's user id and that allows us to access the Admin page.


Flag: `picoCTF{1_id_to_rule_them_all_d77c1ed6}`
