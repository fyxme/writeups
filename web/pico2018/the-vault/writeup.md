> The Vault - Points: 250 - (Solves: 892)
> There is a website running at http://2018shell1.picoctf.com:49030 (link). Try to see if you can login!

Another SQL injection except this time they are checking for SQLI by looking for an `or` statement in the query.

But we don't need the `or` statement in this case and case we can just provide a username and comment out the rest of the statement with this input as the username: `admin' --`

And we get logged in to admin and get the flag.

Flag: `picoCTF{w3lc0m3_t0_th3_vau1t_c4738171}`
