> Logon - Points: 150 - (Solves: 408)
> I made a website so now you can log on to! I don't seem to have the admin password. See if you can't get to the flag. http://2018shell1.picoctf.com:5477 (link)

To start off we check for SQL injection by inputing `'` as the username.

This allows us to login but we get a message:
`Success: You logged in! Not sure you'll be able to see the flag though.`

By looking at the cookies we see that there is a cookie with the name `admin` and the value False.

By changing the value to True and reloading the page we get the flag.


Flag: `picoCTF{l0g1ns_ar3nt_r34l_aaaaa17a}`
