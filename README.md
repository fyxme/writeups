# CTF & Wargames - writeups and exploits

This repo contains a few of the ctf and wargames I've participated in. The repo is currently a mess and needs to be cleaned up. Some challenges have the exploits and not the writeup and other have the writeup but no exploit script.

## Folder structure

- `./firehose/` contains all the challenges which have yet to be sorted
- `./<challenge type>/` contain challenges specific to the specified type
    - `./<challenge type>/<ctf name>/` contains all challenges of that type from that specific ctf

## Interesting Writeups

### Binary exploitation

- [Use after free vulnerability with memory leak allowing heap exploit](binary-exploitation/comp6447-binary-exploitation/4/3/writeup.md)
- [Ret2libc using a buffer overflow and information leak](binary-exploitation/comp6447-binary-exploitation/3/nx-2/writeup.md)
- [Format string vulnerability with %n rewrite](binary-exploitation/comp6447-binary-exploitation/3/sploitwarz-aslr/writeup.md)

### Websec

- [SQL injection with strong WAF and IP ban](web-app-security/comp6843-extended-web-application-security-and-testing/ext-break-1.md)
- [Oauth, SAML & XXE challenges](web-app-security/comp6843-extended-web-application-security-and-testing/ext-break-2.md)
- [Multiple XXS, SSRF & LFI vulns](web-app-security/comp6843-extended-web-application-security-and-testing/break-3.md) 
- [Performing recon](web-app-security/comp6843-extended-web-application-security-and-testing/break-1.md)
- [Basic SQL injection](web-app-security/ctflearn/injection-time/writeup.md)


----------

WIP

### Forensics

### Reversing

### Cryptography

### Misc

- [Convert electrical circuit to binary](miscellaneous/csaw2018/short-circuit/writeup.md)

