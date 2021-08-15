COMP6843 Break 1

REDACTED (z0000000) and REDACTED (z0000000)

## RECON
We used passive, Open Source Intelligence by running the <code>ns.agency</code> domain through the following:
* <code>dnsdumpster.com</code>
* <code>google</code>

To make it easier for ourselves, we used <code>sublist3r</code> to query <code>dnsdumpter.com</code> for the domain names, writing them out to an output file.

From the list of subdomains found, we then tested the subdomains to see if they were valid using the provided script <code>check.py</code> with a shell script wrapper to test each subdomain, writing out the results to another output file. This output file is <code>grep</code>'ed to keep those that are Valid subdomains. Each subdomain was then <code>curl</code>ed to view its contents. We also performed a <code>dig TXT</code> against all the subdomains to see if anything is found in the <code>TXT</code> field.

We also ran the <code>ns.agency</code> against <code>censys.io</code> for certificates and checked to find any suspicous looking certificates to domains not already covered.

Using the known subdomains, we retrieved their IP addresses (even though majority of subdomains would be the same IP address, it is not a guarantee) and then <code>curl</code>ed them.

Following this we tried searching the valid subdomains with the <code>/.git</code> path to find if a git repository exists. Those that give us a <code>404</code> error does not get considered but those that give us a permission error to traverse the tree inadvertently tell us that there is a git repository. Observing the <code>/.git/config</code> file tells use the project slug which allows us to browse it (assuming public git repository). We attempted to try other subdirectories and were tempted to bruteforce them but were advised against it.

Following this, we then bruteforced the subdomains with a wordlist to find more subdomains that may not be registered.

The flags found were:
* <code>ns.agency - COMP6443{0d1c0a8f-d4ca-4e6e-982b-d3ef419a9a5f}</code>
This was found directly on the output from <code>dnsdumpster.com</code>.
* <code>2018.ns.agency - COMP6443{aa6c1a49096293519ca45bedc01501d834f1dc0e}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>au01.aws.ns.agency - COMP6443{AC70D672-AAA4-4323-8EBF-E396097771F9}</code>
This was found by <code>dig TXT</code> against the subdomains found and <code>grep</code>ing out the <code>COMP6443</code> flags.
* <code>cactus.ns.agency - COMP6443{91a9c4db5a0297105c210fd4f1ed9dc4ebba9f29}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>dev.ns.agency - COMP6443{b6598782f1cba0229e0c2ce24052cb247d593a76}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>dota.ns.agency - COMP6443{6e8fd977ee2ffad2aa180f64094f72a4d847cf21}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>en-us.ns.agency - COMP6443{8759c0a1e6c241c6428374b72d754701de93341f}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>7xxxxxxxml.redline.eu.ns.agency - COMP6443{24e9799a7e5c829775bd46b813bec84dec6219ac}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>marketing.ns.agency - COMP6443{387a788f85ecb66422d14f45557d45db1e4c4486}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>notmonitoringyourinternettraffic.ns.agency - COMP6443{f288c7441233897e4b335f2a1840de1ae1dbba21}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>qa.ns.agency - COMP6443{e6a9d29aebad56873fe730daf3312ed6b01e0e0c}</code>
This was found by <code>curl</code>ing the subdomain.
* <code>783883deb90c69709c4204c09e8ae87d.ssl.ns.agency - COMP6443{d6ae6604f9ec13e941e090251bf8ea7c01ad2d37}</code>
This was found by firstly <code>curl</code>ing the subdomain, which left a link pointing to a <code>https</code> link. Upon opening that link, the flag was revealed.
* <code>51a55a0e3c1efe4cbf5cf569a726a35e-js.ns.agency - COMP6443{5a121fb0-4aac-4664-89d4-20385a07cfec}</code>
This was found by observing <code>censys.io</code> and picking out the suspicious looking domain. Examinig the domain revealed a file tree with <code>flag.txt</code> in it which contained the flag.
* <code>ec2-13-238-81-98.ap-southeast-2.compute.amazonaws.com - COMP6443{bea725dd9d91a78afaf067e953c3587777362ccd}</code>
This flag was found getting the IP address of <code>ns.agency</code> and then performing a reverse DNS lookup against it with <code>dig +short -x 13.238.81.98</code>. This revealed the above servername and then <code>curl</code>ing it revealed the flag.
* <code>ns.agency/.git - COMP6443{07b97691-6173-47b3-b1a9-3133db2fa587}
</code>
This flag was found by finding the git repository on <code>ns.agency/.git</code>. Observing the commit history from <code>/.git/logs/HEAD</code> shows us that the second commit removed "private" data. Observing the diff on this commit shows the deleted <code>flag.txt</code> file which held the flag.
* <code>aus.ns.agency - COMP6443{68735dc042f81ec0a05d9577a8c4aa46aeba4634}</code>
This subdomain was found from the word list bruteforce and the flag was found by <code>curl</code>ing the site.
* <code>broken.ns.agency - COMP6443{763029311136584ebc0e0a7027aee65767e12d3b}</code>
This subdomain was found from the word list bruteforce and the flag was found by <code>curl</code>ing the site.
* <code>cat.ns.agency - COMP6443{6269baf868d02bf59261cc785b18e8e5ccf19688}</code>
This subdomain was found from the word list bruteforce and the flag was found by <code>curl</code>ing the site.
* <code>kb.ns.agency - COMP6443{4133-8e3e-9d121581c6a5}</code>
This subdomain was found from the word list bruteforce and the flag was found by using Burp Suite to spider the subdomain which revealed a file called <code>oh-a-flag.txt</code> under the <code>/sys</code> directory. The contents of this file contained the above flag.
* <code>Account.ns.agency - COMP6443{abdca219c986c36774f0398b3ec583b61a727faa}</code>
This subdomain was found from the word list bruteforce. <code>curl</code>ling the site led to certificate errors, so the subdomain was opened in a browser and ignoring the safety warning for invalid certificate, which revealed the flag. 


## EXPLOIT

* <code>login.ns.agency - COMP6443{c966e3ff6076382991478001d5c2fb7c5db7141e}</code>
This was found by injecting <code>' or '1'='1</code> into the password field.

* <code>bread.ns.agency - COMP6443{d7702bc0-1c3e-42ec-a3fc-95c116c90e64} </code>


We have an admin login with username and password input. We start testing possible SQL injections to see if the route is vulnerable. We test for error based and sleep based SQLi but both return nothing. It looks like a dead end.
By analysing the requests and responses we realise cookies are being set on each requests.


Here is the response from a simple GET request:

```bash
% curl -I http://bread.ns.agency/      
HTTP/1.1 200 OK
Date: Mon, 04 Mar 2019 03:02:54 GMT
Server: gunicorn/19.9.0
Content-Type: text/html; charset=utf-8
Content-Length: 2454
Set-Cookie: session=123; Path=/
Vary: Accept-Encoding
```

As we can see a cookie name __session__ is being set to 123.

We start trying to enumerate the users by setting the cookies to differents alphanumeric values. (a, b, c, 0, 1, 2, 3, admin, etc).
Nothing is returned.

We then set the value to be `})'"; -` to see if we can get it to break.

Success! We get an error page where we can see the SQL statement being run: 
`select * from admins where session = \'})\'" -\'`

From there it's easy to form set our session cookie to exploit the SQL query.

By setting the value to `' or 1='1` we expect the SQL statement to be `select * from admins where session = '' or 1='1'`

We request the page again with our new session value and we get access to the admin page! 

```bash
% http GET http://bread.ns.agency/ Cookie:session="' or 1='1" | grep COMP6443

<code style="font-size: 1.5rem">COMP6443{d7702bc0-1c3e-42ec-a3fc-95c116c90e64}</code>
```
