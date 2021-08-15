> Mr. Robots - Points: 200 - (Solves: 459)
> Do you see the same things I see? The glimpses of the flag hidden away? http://2018shell1.picoctf.com:60945 (link)

The title is already an indicator of where we should look.

Looking for the robots.txt at `http://2018shell1.picoctf.com:60945/robots.txt` returns:
```
User-agent: *
Disallow: /65c0c.html
```

We can follow the disallowed link to `http://2018shell1.picoctf.com:60945/65c0c.html` and we get the flag.

Flag: `picoCTF{th3_w0rld_1s_4_danger0us_pl4c3_3lli0t_65c0c}`
