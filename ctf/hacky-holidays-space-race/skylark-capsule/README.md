# Skylark Capsule

![](Pasted%20image%2020210809192708.png)

*TLDR: This is a 2 step challenge where the first steps consist in crack a JWT token and crafting a modified JWT token. The second steps consists of finding a CRC-32 hash collision in order to login to the admin account.*

The website is pretty empty when you navigate to it: 
![](Pasted%20image%2020210809193913.png)

We navigate to register and sign up with the following credentials `hello:hello`:
![](Pasted%20image%2020210809194246.png)

We navigate to capsule in order and find a get specs button:
![](Pasted%20image%2020210809194344.png)

Clicking on this button gives us a generic message without much context:
```
Successfully retrieved and reviewed your specs. You are all ready for launch.
```

By inspecting the request we see that the website appears to be using JWTs (furthermore the Angular favicon hints that this is a frontend application and therefore may be using JWTs):

![](Pasted%20image%2020210809194600.png)

We can decode quickly in the terminal by splitting on the dots (.), base64 decoding each parts and redirecting errors to `/dev/null`:
```
$ for i in `echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjo2LCJ1c2VybmFtZSI6ImhlbGxvIiwiZW1haWwiOiJoZWxsbyIsInBhc3N3b3JkIjoiOTA3MDYwODcwIn0sImlhdCI6MTYyODUwMjE3NX0.t6P8-epQ1zXUbdgXaA7vQ67JP0ZWE8sy0RaVt55s8Y4" | tr "." "\n"`; do echo $i | base64 -d 2&>/dev/null; done
{"alg":"HS256","typ":"JWT"}{"data":{"id":6,"username":"hello","email":"hello","password":"907060870"},"iat":1628502175}
```

The JWT appears to be storing the email, the username and the password hash.

Try to set the algorithm to None didn't work, however since this is an HS256 token, it's signed using a secret and we can therefore try to bruteforce the secret key.

We can use hashcat to bruteforce the key as such:
```
# -m 16500 for JWT token mode
% hashcat -m 16500 -a 0 hash.txt /usr/share/wordlists/rockyou.txt --force
hashcat (v5.1.0) starting...

OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Core(TM) i7-8665U CPU @ 1.90GHz, 2048/5918 MB allocatable, 3MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers:
* Zero-Byte
* Not-Iterated
* Single-Hash
* Single-Salt

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

* Device #1: build_opts '-cl-std=CL1.2 -I OpenCL -I /usr/share/hashcat/OpenCL -D LOCAL_MEM_TYPE=2 -D VENDOR_ID=64 -D CUDA_ARCH=0 -D AMD_ROCM=0 -D VECT_SIZE=8 -D DEVICE_TYPE=2 -D DGST_R0=0 -D DGST_R1=1 -D DGST_R2=2 -D DGST_R3=3 -D DGST_ELEM=16 -D KERN_TYPE=16511 -D _unroll'
Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjo2LCJ1c2VybmFtZSI6ImhlbGxvIiwiZW1haWwiOiJoZWxsbyIsInBhc3N3b3JkIjoiOTA3MDYwODcwIn0sImlhdCI6MTYyODUwMjE3NX0.t6P8-epQ1zXUbdgXaA7vQ67JP0ZWE8sy0RaVt55s8Y4:skylark140584

Session..........: hashcat
Status...........: Cracked
Hash.Type........: JWT (JSON Web Token)
Hash.Target......: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Im...55s8Y4
Time.Started.....: Mon Aug  9 19:53:16 2021 (3 secs)
Time.Estimated...: Mon Aug  9 19:53:19 2021 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1062.3 kH/s (2.22ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 3707904/14344385 (25.85%)
Rejected.........: 0/3707904 (0.00%)
Restore.Point....: 3704832/14344385 (25.83%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: slabriderpro -> skykin

Started: Mon Aug  9 19:53:14 2021
Stopped: Mon Aug  9 19:53:20 2021
%                                                  
```

Using jwt.io we craft a JWT token with the admin's username and id 1 (we assume id 1 is the admin):
![](Pasted%20image%2020210809200049.png)

We use Burp Repeater to replay the `GET /user/capsule` request with our newly crafted token and we get our first flag:
![](Pasted%20image%2020210809200213.png)

We also get the admin's username, email and password "hash":
```
{
	"id":4,
	"username":"admin",
	"email":"admin@spacerace.com",
	"password":"-432570933"
}
```

![](Pasted%20image%2020210809201712.png)

The challenge description gives us a hint that this is a `non-cryptographic hashing algorithm`.

Looking at the non-cryptographic hash types, the first thing that comes up is CRC (Cyclic redundancy checks):

![](Pasted%20image%2020210809202017.png)

CRC-32 also appears to match our hash length.

From our earlier account, we know that the password `hello` hashes to `907060870`:
```
{"id":6,"username":"hello","email":"hello","password":"907060870"},"iat":1628502175}
```

Using ipython we can confirm that this is actually a CRC-32 hash: 
```
In [1]: import binascii

In [2]: print(binascii.crc32("hello"))
907060870
```

We know that the admin password has a CRC-32 hash of "-432570933" and since a CRC-32 hash length is only 32 bits and that its a non-cryptographic hashing algorithm, we can assume that we have to find a hash collision that matches "-432570933" to login to the admin's account.

Python CRC-32 hashing prior to python 3 used to allow negative CRC-32 checksums because it was using signed integers to store the result of the checksum. However, CRC-32 should only return unsigned integers. Hence, we need to convert it.

Using bit manipulation, we can convert it from an signed integer to an unsigned int:
```
In [3]: print -432570933 & 0xffffffff
3862396363
```

So if we manage to find a hash collision for 3862396363, we can use that to login as the admin user.

We couldn't find a program for this so we decide to write our own:
https://github.com/fyxme/crc-32-hash-collider

When we run it, we get a collision back pretty quickly:
```
$ go run collide.go
Collision found: 4iSg@
```

Again we can verify this collision hashes to "-432570933" using python:
```
In [1]: import binascii
In [2]: print(binascii.crc32("4iSg@"))
-432570933
```

Lastly we login to the web application as the admin user using `4iSg@` as the password.

This gives us our second and final flag for this challenge:
![](Pasted%20image%2020210809204115.png)
