> Artisinal Handcrafted HTTP 3 - Points: 300 - (Solves: 251)
> We found a hidden flag server hiding behind a proxy, but the proxy has some... _interesting_ ideas of what qualifies someone to make HTTP requests. Looks like you'll have to do this one by hand. Try connecting via nc 2018shell1.picoctf.com 33281, and use the proxy to send HTTP requests to `flag.local`. We've also recovered a username and a password for you to use on the login page: `realbusinessuser`/`potoooooooo`.

Part 1: get index page
```
Real Business Corp., Internal Proxy
Version 2.0.7
To proceed, please solve the following captcha:

 __             _____
/  |           |  ___|  ______
`| |   ______  |___ \  |______|
 | |  |______|     \ \  ______
_| |_          /\__/ / |______|
\___/          \____/




> -4
Validation succeeded.  Commence HTTP.

GET / HTTP/1.1
Host: flag.local

HTTP/1.1 200 OK
x-powered-by: Express
content-type: text/html; charset=utf-8
content-length: 321
etag: W/"141-LuTf9ny9p1l454tuA3Un+gDFLWo"
date: Tue, 02 Oct 2018 13:53:37 GMT
connection: close


                <html>
                        <head>
                                <link rel="stylesheet" type="text/css" href="main.css" />
                        </head>
                        <body>
                                <header>
                                        <h1>Real Business Internal Flag Server</h1>
                                        <a href="/login">Login</a>
                                </header>
                                <main>
                                        <p>You need to log in before you can see today's flag.</p>
                                </main>
                        </body>
                </html>
```

Part 2: Submit user and pass to /login
```
Real Business Corp., Internal Proxy
Version 2.0.7
To proceed, please solve the following captcha:

   ___            ______
  /   |          |___  /  ______
 / /| |  ______     / /  |______|
/ /_| | |______|   / /    ______
\___  |          ./ /    |______|
    |_/          \_/




> -3
Validation succeeded.  Commence HTTP.

POST /login HTTP/1.1
Host: flag.local
Content-type: application/x-www-form-urlencoded
Content-length: 38

user=realbusinessuser&pass=potoooooooo
HTTP/1.1 302 Found
x-powered-by: Express
set-cookie: real_business_token=PHNjcmlwdD5hbGVydCgid2F0Iik8L3NjcmlwdD4%3D; Path=/
location: /
vary: Accept
content-type: text/plain; charset=utf-8
content-length: 23
date: Tue, 02 Oct 2018 14:01:12 GMT
connection: close

Found. Redirecting to /
```


Finally get the index page with the cookie set:
```
Real Business Corp., Internal Proxy
Version 2.0.7
To proceed, please solve the following captcha:

 _____           _____
/ __  \    _    |  _  |  ______
`' / /'  _| |_  | |_| | |______|
  / /   |_   _| \____ |  ______
./ /___   |_|   .___/ / |______|
\_____/         \____/




> 11
Validation succeeded.  Commence HTTP.

GET / HTTP/1.1
Host: flag.local
Cookie: real_business_token=PHNjcmlwdD5hbGVydCgid2F0Iik8L3NjcmlwdD4%3D

HTTP/1.1 200 OK
x-powered-by: Express
content-type: text/html; charset=utf-8
content-length: 438
etag: W/"1b6-aTY4OAmystMcPatyLXTqxA5wvN4"
date: Tue, 02 Oct 2018 14:03:28 GMT
connection: close


                <html>
                        <head>
                                <link rel="stylesheet" type="text/css" href="main.css" />
                        </head>
                        <body>
                                <header>
                                        <h1>Real Business Internal Flag Server</h1>
                                        <div class="user">Real Business Employee</div>
                                        <a href="/logout">Logout</a>
                                </header>
                                <main>
                                        <p>Hello <b>Real Business Employee</b>!  Today's flag is: <code>picoCTF{0nLY_Us3_n0N_GmO_xF3r_pR0tOcol5_251f}</code>.</p>
                                </main>
                        </body>
                </html>
```

Flag: `picoCTF{0nLY_Us3_n0N_GmO_xF3r_pR0tOcol5_251f}`
