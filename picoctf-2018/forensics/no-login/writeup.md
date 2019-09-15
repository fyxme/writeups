> No Login - Points: 200 - (Solves: 205)
> Looks like someone started making a website but never got around to making a login, but I heard there was a flag if you were the admin. http://2018shell1.picoctf.com:52920 (link)

From inspecting the code, there doesn't seem to be any javascript or any hidden urls we can navigate to.

When we navigate to `/flag` there is a message saying we are not the admin.

The `/login` address doesn't exist so maybe they are checking for a specific cookie to be set.

We set the cookie `admin=True` and navigate again to `/flag`.

And bingo we get the flag!

Flag: `picoCTF{n0l0g0n_n0_pr0bl3m_3184f702}`
